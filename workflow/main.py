from prefect.client.schemas.schedules import CronSchedule
from prefect.docker import DockerImage
from src.services.hackernews import run_hn_flow
from src.services.techcrunch import run_tc_flow
from src.services.supabase_cleanup import cleanup_audio_files
if __name__ == "__main__":

    # # Hacker News flow
    run_hn_flow.deploy(name="HN-ACR",
                work_pool_name="my-aci-pool",
                image=DockerImage(name="hacker-news-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
                schedules= [CronSchedule(cron="0 7 * * *", timezone="America/Los_Angeles")]
                )

    # # TechCrunch AI Article Summary flow
    run_tc_flow.deploy(name="TC-Summary",
            work_pool_name="my-aci-pool",
            image= DockerImage(name="tc-summary-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
            schedules= [CronSchedule(cron="30 7 * * *", timezone="America/Los_Angeles")]
            )
    
    # Cleanup audio files flow
    cleanup_audio_files.deploy(name="Cleanup-Audio-Files",
            work_pool_name="my-aci-pool",
            image= DockerImage(name="cleanup-audio-files-image:v1.0.0", platform="linux/amd64", dockerfile="Dockerfile"),
            schedules= [CronSchedule(cron="0 10 * * *", timezone="America/Los_Angeles")]
            )
