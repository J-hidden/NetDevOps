from collect_info.ap_colle import collect_aps
from collect_info.cpu_uage_coll import collect_cpu_info
from collect_info.intf_colle import collect_intfs
from collect_info.neighbor_lldp_coll import neighbor_lldp_coll
from collect_info.transceiver_verbose_coll import transceiver_coll, transceiver__verbose_coll
from collect_info.version_coll import collect_versions
import time
import schedule


def tasklist():
    schedule.clear()
    schedule.every(10).second.do(collect_aps)
    schedule.every(10).second.do(collect_cpu_info)
    schedule.every(10).second.do(collect_intfs)
    schedule.every(10).second.do(neighbor_lldp_coll)
    schedule.every(10).second.do(transceiver_coll)
    schedule.every(10).second.do(transceiver__verbose_coll)
    schedule.every(10).second.do(collect_versions)
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    tasklist()