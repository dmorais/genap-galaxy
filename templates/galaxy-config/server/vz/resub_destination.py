from galaxy.jobs import JobDestination
from galaxy.jobs.mapper import JobMappingException
import logging
import datetime
from ConfigParser import SafeConfigParser

log = logging.getLogger(__name__)

UPLOAD_TOOLS = ('upload1', 'upload_local_file', 'ucsc_table_direct1', 'ucsc_table_direct_test1', 'ucsc_table_direct_archaea1', 'microbial_import1', 'modENCODEfly',
                    'modENCODEworm')
def dynamic_queue_ip07 (user_email, tool,tool_id, job, app):

    parse = get_ini()
    launch_time = str(datetime.datetime.now())

    param_dict = dict([(p.name, p.value) for p in job.parameters])
    param_dict = tool.params_from_strings(param_dict, app)

    if '/' in tool.id:
        tool_id = tool.id.split('/')[-2]

    ## For upload tools ###
    if tool_id in UPLOAD_TOOLS:
        destination = app.job_config.get_destination(parse.get('upload', 'queue'))

        message = launch_time[:-4] +  ' job_id=' + str(job.id) + ' ' + parse.get('upload', 'walltime') + ' ' + \
                  parse.get('upload', 'pmem') + ' ' +  parse.get('upload', 'cores') + ' destination=' + \
                  parse.get('upload', 'queue') + ' tool_id=' + tool_id + "\n"

        print_log(message)
        print message
        print destination, "job_id=" + str(job.id), "tool_id=" + tool_id
        return destination

    if '__job_resource' in param_dict:
        if param_dict['__job_resource']['__job_resource__select'] == 'yes':

            if param_dict['__job_resource']['queue'] in parse.sections():
                section = param_dict['__job_resource']['queue']
                destination = app.job_config.get_destination( parse.get(section, 'queue'))

                # if a destination is selected and other param are specified
                if param_dict['__job_resource']['time'] >=1 and param_dict['__job_resource']['memory'] >= 1 and \
                        param_dict['__job_resource']['processors'] >= 1:

                    walltime = param_dict['__job_resource']['time']
                    memory = param_dict['__job_resource']['memory'] * 1000
                    cores = param_dict['__job_resource']['processors']

                    # custom job destination and parameters
                    message =  launch_time[:-4] + ' job_id=' + str(job.id) +  ' walltime=' + str(walltime) + ':00:00 pmem=' + \
                               str(memory) + ' -l nodes=1:ppn=' + str(cores) + ' destination=' +  parse.get(section, 'queue') + ' tool_id='+ tool_id + "\n"


                    print section,  'job_id' + str(job.id), 'tool_id=' + tool_id
                    print_log(message)
                    print message
                    return destination

                elif param_dict['__job_resource']['time'] == -1:

                    # if a destination is selected but no other param is selected
                    message = launch_time[:-4] +  ' job_id=' + str(job.id) + ' ' + parse.get(section, 'walltime') + ' ' + \
                    parse.get(section, 'pmem') + ' ' +  parse.get(section, 'cores') + ' destination=' + \
                    parse.get(section, 'queue') + ' tool_id=' + tool_id + "\n"

                    print_log(message)
                    print message
                    return destination


    # If no job resource param is selected
    message = launch_time[:-4] + ' job_id=' + str(job.id) + ' ' + parse.get('DEFAULT', 'walltime') + ' ' + \
    parse.get('DEFAULT', 'pmem') + ' ' +  parse.get('DEFAULT', 'cores') + ' destination=' + \
    parse.get('DEFAULT', 'queue') + ' tool_id=' + tool_id + "\n"

    destination_id = parse.get('DEFAULT', 'queue')
    print_log(message)
    print message
    return destination_id

def print_log(message):
    with open('/var/log/job_destination.log', 'ab+') as f:
        f.write(message)

def get_ini():
    # read config file with queue options
    parser = SafeConfigParser()
    parser.read('/ramdisk/galaxy/0.6/galaxy-dist/config/cluster.ini')
    return parser
