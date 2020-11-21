import threading

from ZotikosManager.controllers.device_monitor_task import DeviceMonitorTask
from ZotikosManager.controllers.compliance_monitor_task import ComplianceMonitorTask
from ZotikosManager.controllers.configuration_monitor_task import ConfigurationMonitorTask
from ZotikosManager.controllers.utils import log_console


class ThreadManager:
    device_monitor_task = None
    device_monitor_thread = None
    compliance_monitor_task = None
    compliance_monitor_thread = None
    config_monitor_task = None
    config_monitor_thread = None

    @staticmethod
    def stop_device_threads():
        log_console(f"Shutting down device monitoring threads")

        if ThreadManager.device_monitor_task and ThreadManager.device_monitor_thread:
            ThreadManager.device_monitor_task.set_terminate()
            ThreadManager.device_monitor_thread.join()

        if ThreadManager.compliance_monitor_task and ThreadManager.compliance_monitor_thread:
            ThreadManager.compliance_monitor_task.set_terminate()
            ThreadManager.config_monitor_thread.join()

        if ThreadManager.config_monitor_task and ThreadManager.config_monitor_thread:
            ThreadManager.config_monitor_task.set_terminate()
            ThreadManager.config_monitor_thread.join()

        ThreadManager.device_monitor_task = None
        ThreadManager.device_monitor_thread = None
        ThreadManager.compliance_monitor_task = None
        ThreadManager.config_monitor_thread = None
        ThreadManager.config_monitor_task = None
        ThreadManager.config_monitor_thread = None

    @staticmethod
    def start_device_threads(device_monitor_interval=60, compliance_monitor_interval=60, config_monitor_interval=60):

        ThreadManager.device_monitor_task = DeviceMonitorTask()
        ThreadManager.device_monitor_thread = threading.Thread(
            target=ThreadManager.device_monitor_task.monitor,
            args=(device_monitor_interval,),
        )
        ThreadManager.device_monitor_thread.start()

        ThreadManager.compliance_monitor_task = ComplianceMonitorTask()
        ThreadManager.compliance_monitor_thread = threading.Thread(
            target=ThreadManager.compliance_monitor_task.monitor,
            args=(compliance_monitor_interval,),
        )
        ThreadManager.compliance_monitor_thread.start()

        ThreadManager.config_monitor_task = ConfigurationMonitorTask()
        ThreadManager.config_monitor_thread = threading.Thread(
            target=ThreadManager.config_monitor_task.monitor,
            args=(config_monitor_interval,),
        )
        ThreadManager.config_monitor_thread.start()

    @staticmethod
    def initiate_terminate_all_threads():
        if ThreadManager.device_monitor_task and ThreadManager.device_monitor_thread:
            ThreadManager.device_monitor_task.set_terminate()

        if ThreadManager.compliance_monitor_task and ThreadManager.compliance_monitor_thread:
            ThreadManager.compliance_monitor_task.set_terminate()

        if ThreadManager.config_monitor_task and ThreadManager.config_monitor_thread:
            ThreadManager.config_monitor_task.set_terminate()
