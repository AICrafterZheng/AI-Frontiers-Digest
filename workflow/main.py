from prefect.client.schemas.schedules import CronSchedule
from prefect.docker import DockerImage
from src.services.hn_service import run_hn_flow, run_test_hn_flow
from src.services.tc_service import run_tc_flow, run_test_tc_flow
if __name__ == "__main__":
    import asyncio
    # Enable to run locally
    # asyncio.run(HackerNewsService().run_test_flow())
    # asyncio.run(run_test_hn_flow())
    asyncio.run(run_test_tc_flow())

    # cron = CronSchedule(cron="0 7 * * *", timezone="America/Los_Angeles")
    # # # Hacker News flow
    # run_hn_flow.deploy(name="HN-ACR",
    #             work_pool_name="my-aci-pool",
    #             image=DockerImage(name="hacker-news-image:v1.0.0", platform="linux/amd64"),
    #             schedules= [cron]
    #             )


    # # # TechCrunch AI Article Summary flow
    # run_tc_flow.deploy(name="TC-Summary-ACR",
    #         work_pool_name="my-aci-pool",
    #         image= DockerImage(name="tc-summary-image:v1.0.0", platform="linux/amd64"),
    #         schedules= [cron]
    #         )
