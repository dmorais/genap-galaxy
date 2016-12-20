from galaxy.jobs import JobDestination
from galaxy.jobs.mapper import JobMappingException
import logging
import datetime

log = logging.getLogger(__name__)

DESTINATION_DEFAULT = 'metaq'
DESTINATION_DYNAMIC = 'qdynamic'
DESTINATIONS_VZ = ('qtest3_short', 'qtest3' )
UPLOAD_TOOLS = ('upload1', 'upload_local_file', 'ucsc_table_direct1', 'ucsc_table_direct_test1', 'ucsc_table_direct_archaea1', 'microbial_import1', 'modENCODEfly',
'modENCODEworm')


def dynamic_McGill_queue (user_email, tool,tool_id, job, app):
    
    launch_time = str(datetime.datetime.now())
    memory = '1000'
    cores = '1'
    walltime = '72'
    param_dict = dict( [ ( p.name, p.value ) for p in job.parameters ] )
    param_dict = tool.params_from_strings( param_dict, app )
    if '/' in tool.id:
        tool_id = tool.id.split('/')[-2]    
    ## For upload tools ###
    if tool_id in UPLOAD_TOOLS:
        destination = app.job_config.get_destination( DESTINATION_DYNAMIC )
        destination.params['Resource_List'] = "walltime=36:00:00, -l node=1:ppn=1" 
        #destination_id = 'qtest3_short'
        message = launch_time[:-4] +  " job_id=" + str(job.id) +  " walltime=36:00:00 pmem=32000 -l nodes=1:ppn=1" +  " destination=" + destination.params['destination'] +  " tool_id="+ tool_id + "\n"
        print_log_McGill(message)
        print destination, "job_id=" + str(job.id), "tool_id=" + tool_id
        return destination
    
    if '__job_resource' in param_dict:
        if param_dict['__job_resource']['__job_resource__select'] == 'yes':
            destination = app.job_config.get_destination( DESTINATION_DYNAMIC )

            if param_dict['__job_resource']['time'] >= 1 :
                walltime = param_dict['__job_resource']['time']
            if param_dict['__job_resource']['memory'] >= 1 :
                 memory = param_dict['__job_resource']['memory'] * 1000
            if param_dict['__job_resource']['processors'] >= 1 :
                 cores = param_dict['__job_resource']['processors']
        else:
            print "Sending tool %s job %s to %s (default destination)" % (tool_id, job.id, DESTINATION_DEFAULT)
            message = launch_time[:-4] +  " job_id=" + str(job.id) +  " walltime=72:00:00 pmem=32000 -l nodes=1:ppn=24" +  " destination=" + DESTINATION_DEFAULT +  " tool_id="+ tool_id + "\n"
            print_log_McGill(message)
            destination_id = DESTINATION_DEFAULT
            return destination_id

        destination.params['Resource_List'] = "walltime=%s:00:00,pmem=%s,-l node=1:ppn=%s" % (str(walltime), str(memory), str(cores))
        message =  launch_time[:-4] + " job_id=" + str(job.id) +  " walltime=" + str(walltime) + " pmem=" + str(memory) +  " -l node=1:ppn=" + str(cores) + " destination=" + destination.params['destination'] + " tool_id="+ tool_id + "\n"
        print destination, "job_id" + str(job.id), "tool_id=" + tool_id
        print_log_McGill(message)
        return destination

    else:
        print "Sending tool %s job %s to %s (default destination)" % (tool_id, job.id, DESTINATION_DEFAULT)
        message = launch_time[:-4] +  " job_id=" + str(job.id) +  " walltime=72:00:00 pmem=32000 -l nodes=1:ppn=24" +  " destination=" + DESTINATION_DEFAULT + " tool_id="+ tool_id + "\n"
        print_log_McGill(message)
        destination_id = DESTINATION_DEFAULT
        return destination_id


def print_log_McGill(message):
    with open('/ramdisk/galaxy/0.6/galaxy-dist/job_destination.log', 'ab+') as f:
        f.write(message)

