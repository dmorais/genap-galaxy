from galaxy.jobs import JobDestination
from galaxy.jobs.mapper import JobMappingException
import os
import logging
import datetime

log = logging.getLogger(__name__)

DESTINATION_DEFAULT = 'qsmall'
DESTINATIONS = ('qsmall', 'qbig', 'qmid')

def dynamic_queue_pub (tool,tool_id, job, app):
    WALLTIME = 0
    param_dict = dict( [ ( p.name, p.value ) for p in job.parameters ] )
    param_dict = tool.params_from_strings( param_dict, app )

    if '__job_resource' in param_dict:
        if param_dict['__job_resource']['__job_resource__select'] == 'yes':
            # If time is set assing the value to WALLTIME
            if param_dict['__job_resource']['time']:
                WALLTIME = param_dict['__job_resource']['time']
            resource_key = None
            for resource_key in param_dict['__job_resource'].keys():
                if param_dict['__job_resource'][resource_key] in DESTINATIONS:
                    destination_id = param_dict['__job_resource'][resource_key]
                    break

            else:
                log.warning('(%s) Destination/walltime dynamic plugin got an invalid value for selector: %s \nSending job to %s (default) queue', job.id, param_dict['__job_resource']['__job_resource__select'], DESTINATION_DEFAULT)
                destination_id = 'qsmall'
        elif param_dict['__job_resource']['__job_resource__select'] == 'no':
            destination_id = DESTINATION_DEFAULT

        else:
            destination_id = DESTINATION_DEFAULT
    else:
         log.warning('(%s) Destination/walltime dynamic plugin did not receive the __job_resource param, keys were: %s \nSending job to %s (default) queue', job.id, param_dict.keys(), DESTINATION_DEFAULT)
         destination_id = DESTINATION_DEFAULT
    # IF WALLTIME was set replace default walltime by the new set value
    if WALLTIME > 0 :
        destination = app.job_config.get_destination( destination_id )
        # If the user tries to set a walltime > 48 hour on qsmall, reset to 24 hours
        #if destination_id == 'qsmall':
        #    return destination_id
        # If a user tries to set more than 24 hours on qbig reset to 48 hours
        if destination_id == 'qfat512' and WALLTIME > 24 :
            return destination_id
        # set walltime to the chosen destination
        else:
            destination.params['Resource_List'] = 'walltime=%s:00:00' % str(WALLTIME)
            return destination

    else:
        return destination_id
