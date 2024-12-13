from pydantic import BaseModel

class DailyActivityContributors(BaseModel):
    meet_daily_targets: int
    move_every_hour: int
    recovery_time: int
    stay_active: int
    training_frequency: int
    training_volume: int

class DailyActivity(BaseModel):
    id: str
    score: int
    active_calories: int
    average_met_minutes: float
    contributors: DailyActivityContributors
    equivalent_walking_distance: int
    high_activity_met_minutes: int
    high_activity_time: int
    inactivity_alerts: int
    low_activity_met_minutes: int
    low_activity_time: int
    medium_activity_met_minutes: int
    medium_activity_time: int
    meters_to_target: int
    non_wear_time: int
    resting_time: int
    sedentary_met_minutes: int
    sedentary_time: int
    steps: int
    target_calories: int
    target_meters: int
    total_calories: int
    day: str
    timestamp: str

    @property
    def lookup(self):
        return "daily_activity"