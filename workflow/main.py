from prefect.client.schemas.schedules import CronSchedule
from prefect.docker import DockerImage
from src.services.hn_service import run_hn_flow
from src.services.tc_service import run_tc_flow
if __name__ == "__main__":

    # # Hacker News flow
    run_hn_flow.deploy(name="HN-ACR",
                work_pool_name="my-aci-pool",
                image=DockerImage(name="hacker-news-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
                schedules= [CronSchedule(cron="0 7 * * *", timezone="America/Los_Angeles")]
                )

    # # TechCrunch AI Article Summary flow
    run_tc_flow.deploy(name="TC-Summary-1",
            work_pool_name="my-aci-pool",
            image= DockerImage(name="tc-summary-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
            schedules= [CronSchedule(cron="0 9 * * *", timezone="America/Los_Angeles")]
            )
    # TechCrunch keep posting new articles during the day
    run_tc_flow.deploy(name="TC-Summary-2",
            work_pool_name="my-aci-pool",
            image= DockerImage(name="tc-summary-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
            schedules= [CronSchedule(cron="0 23 * * *", timezone="America/Los_Angeles")]
            )