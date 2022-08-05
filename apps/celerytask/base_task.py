import celery
from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from apps.bussiness.models import TaskLog

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    def run(self, *args, **kwargs):
        super(BaseTask, self).run(*args, **kwargs)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"======= EINFO ======\n{einfo}\n================")
        tl = TaskLog.logic_objects.filter(celery_task_id=task_id).first()
        if not tl:
            logger.error(f"task_id={task_id} 的任务日志在数据库中不存在...")
            return
        tl.is_success = False
        result = AsyncResult(task_id)
        tl.final_status = result.status
        tl.retry_count = tl.retry_count + 1
        tl.result = {"error_info": str(einfo)}
        tl.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"======= EINFO ======\n{einfo}\n================")
        tl = TaskLog.logic_objects.filter(celery_task_id=task_id).first()
        if not tl:
            logger.error(f"task_id={task_id} 的任务日志在数据库中不存在...")
            return
        tl.is_success = False
        result = AsyncResult(task_id)
        tl.final_status = result.status
        tl.result = {"error_info": str(einfo)}
        tl.save()

    def on_success(self, retval, task_id, args, kwargs):
        tl = TaskLog.logic_objects.filter(celery_task_id=task_id).first()
        if not tl:
            logger.error(f"task_id={task_id} 的任务日志在数据库中不存在...")
            return
        tl.is_success = True
        result = AsyncResult(task_id)
        tl.final_status = result.status
        tl.save()

    def before_start(self, task_id, args, kwargs):
        """
        在开始执行之前，创建新的task数据
        """
        tl = TaskLog.init_entity(task_id, self.name, kwargs)
        tl.save()
