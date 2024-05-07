import logging
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TruckData:
    speed: Optional[float] = None  # Truck speed in km/h
    acceleration: Optional[float] = None  # Truck acceleration rate
    brake: Optional[float] = None  # Brake pressure
    engine_rpm: Optional[int] = None  # Engine RPM
    fuel: Optional[float] = None  # Current fuel in liters
    fuel_capacity: Optional[float] = None  # Fuel tank capacity in liters
    fuel_rate: Optional[float] = None  # Fuel consumption rate liters/hour
    wear_engine: Optional[float] = None  # Engine wear and tear percentage
    wear_transmission: Optional[float] = None  # Transmission wear and tear percentage
    wear_cabin: Optional[float] = None  # Cabin wear and tear percentage
    wear_chassis: Optional[float] = None  # Chassis wear and tear percentage
    wear_wheels: Optional[float] = None  # Wheels wear and tear percentage
    lights_dashboard: Optional[int] = None  # Dashboard lights state (0: off, 1: on)
    blinker_left_active: Optional[bool] = None  # Left blinker active state
    blinker_right_active: Optional[bool] = None  # Right blinker active state
    lights_fog: Optional[int] = None  # Fog light state (0: off, 1: on)
    wipers: Optional[bool] = None  # Wipers state
    user_steer: Optional[float] = None
    user_throttle: Optional[float] = None
    user_brake: Optional[float] = None
    user_clutch: Optional[float] = None
    game_steer: Optional[float] = None
    game_throttle: Optional[float] = None
    game_brake: Optional[float] = None
    game_clutch: Optional[float] = None
    cruise_control_speed: Optional[float] = None
    air_pressure: Optional[float] = None
    brake_temperature: Optional[float] = None
    fuel_avg_consumption: Optional[float] = None
    fuel_range: Optional[float] = None
    adblue: Optional[float] = None
    oil_pressure: Optional[float] = None
    oil_temperature: Optional[float] = None
    water_temperature: Optional[float] = None
    battery_voltage: Optional[float] = None
    truck_odometer: Optional[float] = None
    speed_limit: Optional[float] = None
    refuel_amount: Optional[float] = None
    is_cargo_loaded: Optional[bool] = None
    park_brake: Optional[bool] = None
    motor_brake: Optional[bool] = None
    air_pressure_warning: Optional[bool] = None
    air_pressure_emergency: Optional[bool] = None
    fuel_warning: Optional[bool] = None
    adblue_warning: Optional[bool] = None
    oil_pressure_warning: Optional[bool] = None
    water_temperature_warning: Optional[bool] = None
    battery_voltage_warning: Optional[bool] = None
    electric_enabled: Optional[bool] = None
    engine_enabled: Optional[bool] = None
    lights_parking: Optional[bool] = None
    lights_beam_low: Optional[bool] = None
    lights_beam_high: Optional[bool] = None
    lights_beacon: Optional[bool] = None
    lights_brake: Optional[bool] = None
    lights_reverse: Optional[bool] = None
    lights_hazards: Optional[bool] = None
    cruise_control: Optional[bool] = None
    shifter_toggle: List[Optional[bool]] = None
    differential_lock: Optional[bool] = None
    lift_axle: Optional[bool] = None
    lift_axle_indicator: Optional[bool] = None
    trailer_lift_axle: Optional[bool] = None
    trailer_lift_axle_indicator: Optional[bool] = None
    cabin_position_x: Optional[float] = None
    cabin_position_y: Optional[float] = None
    cabin_position_z: Optional[float] = None
    head_position_x: Optional[float] = None
    head_position_y: Optional[float] = None
    head_position_z: Optional[float] = None
    truck_hook_position_x: Optional[float] = None
    truck_hook_position_y: Optional[float] = None
    truck_hook_position_z: Optional[float] = None
    truck_wheel_position_x: List[Optional[float]] = None
    truck_wheel_position_y: List[Optional[float]] = None
    truck_wheel_position_z: List[Optional[float]] = None
    lv_acceleration_x: Optional[float] = None
    lv_acceleration_y: Optional[float] = None
    lv_acceleration_z: Optional[float] = None
    av_acceleration_x: Optional[float] = None
    av_acceleration_y: Optional[float] = None
    av_acceleration_z: Optional[float] = None
    acceleration_x: Optional[float] = None
    acceleration_y: Optional[float] = None
    acceleration_z: Optional[float] = None
    aa_acceleration_x: Optional[float] = None
    aa_acceleration_y: Optional[float] = None
    aa_acceleration_z: Optional[float] = None
    cabin_av_x: Optional[float] = None
    cabin_av_y: Optional[float] = None
    cabin_av_z: Optional[float] = None
    cabin_aa_x: Optional[float] = None
    cabin_aa_y: Optional[float] = None
    cabin_aa_z: Optional[float] = None
    cabin_offset_x: Optional[float] = None
    cabin_offset_y: Optional[float] = None
    cabin_offset_z: Optional[float] = None
    cabin_offset_rotation_x: Optional[float] = None
    cabin_offset_rotation_y: Optional[float] = None
    cabin_offset_rotation_z: Optional[float] = None
    head_offset_x: Optional[float] = None
    head_offset_y: Optional[float] = None
    head_offset_z: Optional[float] = None
    head_offset_rotation_x: Optional[float] = None
    head_offset_rotation_y: Optional[float] = None
    head_offset_rotation_z: Optional[float] = None
    coordinate_x: Optional[float] = None
    coordinate_y: Optional[float] = None
    coordinate_z: Optional[float] = None
    rotation_x: Optional[float] = None
    rotation_y: Optional[float] = None
    rotation_z: Optional[float] = None
    truck_brand_id: Optional[str] = None
    truck_brand: Optional[str] = None
    truck_id: Optional[str] = None
    truck_name: Optional[str] = None
    truck_license_plate: Optional[str] = None
    truck_license_plate_country_id: Optional[str] = None
    truck_license_plate_country: Optional[str] = None
    shifter_type: Optional[str] = None
    truck_wheel_count: Optional[int] = None
    truck_wheel_steerable: List[Optional[bool]] = None
    truck_wheel_simulated: List[Optional[bool]] = None
    truck_wheel_powered: List[Optional[bool]] = None
    truck_wheel_liftable: List[Optional[bool]] = None
    truck_wheel_on_ground: List[Optional[bool]] = None
    truck_wheel_substance: List[Optional[int]] = None
    truck_wheel_radius: List[Optional[float]]
    truck_wheel_radius: List[Optional[float]] = None
    truck_wheel_susp_deflection: List[Optional[float]] = None
    truck_wheel_velocity: List[Optional[float]] = None
    truck_wheel_steering: List[Optional[float]] = None
    truck_wheel_rotation: List[Optional[float]] = None
    truck_wheel_lift: List[Optional[float]] = None
    truck_wheel_lift_offset: List[Optional[float]] = None
    coordinate_x: Optional[float] = None
    coordinate_y: Optional[float] = None
    coordinate_z: Optional[float] = None
    rotation_x: Optional[float] = None
    rotation_y: Optional[float] = None
    rotation_z: Optional[float] = None


@dataclass
class GameData:
    time: Optional[str] = None  # In-game time as a string
    timezone_offset: Optional[int] = None  # Timezone offset in minutes
    next_rest_stop: Optional[int] = None  # Time until next mandatory rest in minutes
    version: Optional[str] = None  # Telemetry server version
    game_paused: Optional[bool] = None  # Is the game paused
    sdk_active: Optional[bool] = None
    simulated_time: Optional[int] = None
    render_time: Optional[int] = None
    multiplayer_time_offset: Optional[int] = None
    telemetry_plugin_revision: Optional[int] = None
    version_major: Optional[int] = None
    version_minor: Optional[int] = None
    game: Optional[int] = None
    telemetry_version_game_major: Optional[int] = None
    telemetry_version_game_minor: Optional[int] = None
    time_abs: Optional[int] = None
    gears: Optional[int] = None
    gears_reverse: Optional[int] = None
    retarder_step_count: Optional[int] = None
    selector_count: Optional[int] = None
    time_abs_delivery: Optional[int] = None
    max_trailer_count: Optional[int] = None
    unit_count: Optional[int] = None
    planned_distance_km: Optional[int] = None
    shifter_slot: Optional[int] = None
    retarder_brake: Optional[int] = None
    lights_aux_front: Optional[int] = None
    lights_aux_roof: Optional[int] = None
    hshifter_position: List[Optional[int]] = None
    hshifter_bitmask: List[Optional[int]] = None
    job_delivered_delivery_time: Optional[int] = None
    job_starting_time: Optional[int] = None
    job_finished_time: Optional[int] = None
    rest_stop: Optional[int] = None
    gear: Optional[int] = None
    gear_dashboard: Optional[int] = None
    hshifter_resulting: List[Optional[int]] = None
    job_delivered_earned_xp: Optional[int] = None
    scale: Optional[float] = None
    fuel_warning_factor: Optional[float] = None
    adblue_capacity: Optional[float] = None
    adblue_warning_factor: Optional[float] = None
    air_pressure_warning: Optional[float] = None
    air_pressure_emergency: Optional[float] = None
    oil_pressure_warning: Optional[float] = None
    water_temperature_warning: Optional[float] = None
    battery_voltage_warning: Optional[float] = None
    engine_rpm_max: Optional[float] = None
    gear_differential: Optional[float] = None
    cargo_mass: Optional[float] = None
    gear_ratios_forward: List[Optional[float]] = None
    gear_ratios_reverse: List[Optional[float]] = None
    unit_mass: Optional[float] = None
    job_delivered_cargo_damage: Optional[float] = None
    job_delivered_distance_km: Optional[float] = None
    cargo_damage: Optional[float] = None
    job_income: Optional[int] = None
    job_cancelled_penalty: Optional[int] = None
    job_delivered_revenue: Optional[int] = None
    fine_amount: Optional[int] = None
    tollgate_pay_amount: Optional[int] = None
    ferry_pay_amount: Optional[int] = None
    train_pay_amount: Optional[int] = None
    on_job: Optional[bool] = None
    job_finished: Optional[bool] = None
    job_cancelled: Optional[bool] = None
    job_delivered: Optional[bool] = None
    fined: Optional[bool] = None
    tollgate: Optional[bool] = None
    ferry: Optional[bool] = None
    train: Optional[bool] = None
    refuel: Optional[bool] = None
    refuel_payed: Optional[bool] = None
    substances: List[Optional[str]] = None


@dataclass
class NavigationData:
    distance: Optional[int] = None  # Distance to destination in meters
    time: Optional[int] = None  # Estimated time to destination in seconds
    route_distance: Optional[float] = None
    route_time: Optional[float] = None
    nearest_cities: List[Dict] = None


@dataclass
class JobData:
    cargo: Optional[str] = None  # Cargo name
    income: Optional[int] = None  # Income from the job
    destination: Optional[str] = None  # Destination city and company
    deadline_time: Optional[str] = None  # Deadline time for job completion
    is_special: Optional[bool] = None  # Is it a special transport job
    cargo_id: Optional[str] = None
    city_dst_id: Optional[str] = None
    city_dst: Optional[str] = None
    comp_dst_id: Optional[str] = None
    comp_dst: Optional[str] = None
    city_src_id: Optional[str] = None
    city_src: Optional[str] = None
    comp_src_id: Optional[str] = None
    comp_src: Optional[str] = None
    job_market: Optional[str] = None
    fine_offence: Optional[str] = None
    ferry_source_name: Optional[str] = None
    ferry_target_name: Optional[str] = None
    ferry_source_id: Optional[str] = None
    ferry_target_id: Optional[str] = None
    train_source_name: Optional[str] = None
    train_target_name: Optional[str] = None
    train_source_id: Optional[str] = None
    train_target_id: Optional[str] = None
    job_autopark_used: Optional[bool] = None
    job_autoload_used: Optional[bool] = None


@dataclass
class TrailerData:
    wheel_steerable: List[Optional[bool]] = None
    wheel_simulated: List[Optional[bool]] = None
    wheel_powered: List[Optional[bool]] = None
    wheel_liftable: List[Optional[bool]] = None
    wheel_on_ground: List[Optional[bool]] = None
    attached: Optional[bool] = None
    wheel_substance: List[Optional[int]] = None
    wheel_count: Optional[int] = None
    cargo_damage: Optional[float] = None
    wear_chassis: Optional[float] = None
    wear_wheels: Optional[float] = None
    wear_body: Optional[float] = None
    wheel_susp_deflection: List[Optional[float]] = None
    wheel_velocity: List[Optional[float]] = None
    wheel_steering: List[Optional[float]] = None
    wheel_rotation: List[Optional[float]] = None
    wheel_lift: List[Optional[float]] = None
    wheel_lift_offset: List[Optional[float]] = None
    wheel_radius: List[Optional[float]] = None
    linear_velocity_x: Optional[float] = None
    linear_velocity_y: Optional[float] = None
    linear_velocity_z: Optional[float]
    linear_velocity_z: Optional[float] = None
    angular_velocity_x: Optional[float] = None
    angular_velocity_y: Optional[float] = None
    angular_velocity_z: Optional[float] = None
    linear_acceleration_x: Optional[float] = None
    linear_acceleration_y: Optional[float] = None
    linear_acceleration_z: Optional[float] = None
    angular_acceleration_x: Optional[float] = None
    angular_acceleration_y: Optional[float] = None
    angular_acceleration_z: Optional[float] = None
    hook_position_x: Optional[float] = None
    hook_position_y: Optional[float] = None
    hook_position_z: Optional[float] = None
    wheel_position_x: List[Optional[float]] = None
    wheel_position_y: List[Optional[float]] = None
    wheel_position_z: List[Optional[float]] = None
    world_x: Optional[float] = None
    world_y: Optional[float] = None
    world_z: Optional[float] = None
    id: Optional[str] = None
    cargo_accessory_id: Optional[str] = None
    body_type: Optional[str] = None
    brand_id: Optional[str] = None
    brand: Optional[str] = None
    name: Optional[str] = None
    chain_type: Optional[str] = None
    license_plate: Optional[str] = None
    license_plate_country: Optional[str] = None
    license_plate_country_id: Optional[str] = None


@dataclass
class TelemetryData:
    truck: Optional[TruckData] = None
    game: Optional[GameData] = None
    navigation: Optional[NavigationData] = None
    job: Optional[JobData] = None
    trailer: List[Optional[TrailerData]] = None


class MockTelemetry:
    def __init__(self):

        self.truck = TruckData(
            speed=80.0,
            acceleration=0.2,
            brake=0.0,
            engine_rpm=1500,
            fuel=800.0,
            fuel_rate=30.0,
            fuel_capacity=1000.0,
            wear_engine=0.0,
            wear_transmission=0.0,
            wear_cabin=0.0,
            wear_chassis=0.0,
            wear_wheels=0.0,
            lights_dashboard=0,
            blinker_left_active=False,
            blinker_right_active=False,
            lights_fog=0,
            wipers=False,
            coordinate_x=2028.0,
            coordinate_y=5855.0,
            coordinate_z=0.0,
            rotation_x=0.0,
            rotation_y=0.0,
            rotation_z=0.0,
        )
        self.game = GameData(
            time="12:00",
            timezone_offset=60,
            next_rest_stop=120,
            version="1.39",
            game_paused=False,
        )
        self.navigation = NavigationData(distance=5000, time=3600)
        self.job = JobData(
            cargo="Electronics",
            income=2000,
            destination="Berlin, Acme Corp",
            deadline_time="2024-05-10T15:00:00",
            is_special=False,
        )
        self.toggle_count = 0

    def update(self):
        # Smooth transitions for speed, acceleration, and engine RPM
        self.truck.speed = max(0, min(100, self.truck.speed + random.uniform(-5, 5)))
        self.truck.acceleration = max(0, random.normalvariate(0.5, 0.1))
        self.truck.engine_rpm = max(
            800, min(3000, self.truck.engine_rpm + random.randint(-100, 100))
        )

        # Realistic coordinates updating based on speed
        self.truck.coordinate_x += self.truck.speed * 0.1
        self.truck.coordinate_y += self.truck.speed * 0.1

        # Decrease fuel based on current fuel rate and speed
        self.truck.fuel = max(
            0, self.truck.fuel - self.truck.fuel_rate * (self.truck.speed / 100) * 0.1
        )
        if self.truck.fuel < 50:  # Refuel scenario
            self.truck.fuel = self.truck.fuel_capacity

        # Increment wear conditionally based on speed
        wear_increment = 0.001 * self.truck.speed / 100
        self.truck.wear_engine = min(100, self.truck.wear_engine + wear_increment)
        self.truck.wear_transmission = min(
            100, self.truck.wear_transmission + wear_increment
        )

        # Toggle blinkers and wipers less frequently
        self.toggle_count += 1
        if self.toggle_count % 10 == 0:  # Every 10 updates, toggle
            self.truck.blinker_left_active = not self.truck.blinker_left_active
            self.truck.blinker_right_active = not self.truck.blinker_left_active
            self.truck.wipers = not self.truck.wipers

        # Update navigation assuming constant speed
        self.navigation.distance = max(
            0, self.navigation.distance - self.truck.speed * 0.1
        )
        if self.navigation.distance == 0:  # Reset for new job scenario
            self.navigation.distance = random.randint(1000, 5000)
            self.navigation.time = random.randint(3000, 7200)

        # logging.debug(
        #     f"All updated fields and values:\n"
        #     f"    truck:\n"
        #     f"      - speed = {self.truck.speed}\n"
        #     f"      - acceleration = {self.truck.acceleration}\n"
        #     f"      - engine_rpm = {self.truck.engine_rpm}\n"
        #     f"      - fuel = {self.truck.fuel}\n"
        #     f"      - wear_engine = {self.truck.wear_engine}\n"
        #     f"      - wear_transmission = {self.truck.wear_transmission}\n"
        #     f"      - wear_cabin = {self.truck.wear_cabin}\n"
        #     f"      - wear_chassis = {self.truck.wear_chassis}\n"
        #     f"      - wear_wheels = {self.truck.wear_wheels}\n"
        #     f"      - lights_dashboard = {self.truck.lights_dashboard}\n"
        #     f"      - blinker_left_active = {self.truck.blinker_left_active}\n"
        #     f"      - blinker_right_active = {self.truck.blinker_right_active}\n"
        #     f"      - lights_fog = {self.truck.lights_fog}\n"
        #     f"      - wipers = {self.truck.wipers}\n"
        #     f"    navigation:\n"
        #     f"      - distance = {self.navigation.distance}\n"
        #     f"      - time = {self.navigation.time}\n"
        #     f"    job:\n"
        #     f"      - cargo = {self.job.cargo}\n"
        #     f"      - income = {self.job.income}\n"
        #     f"      - destination = {self.job.destination}\n"
        #     f"      - deadline_time = {self.job.deadline_time}\n"
        #     f"      - is_special = {self.job.is_special}"
        # )

    def get_telemetry_data(self):
        self.update()
        return TelemetryData(
            truck=self.truck, game=self.game, navigation=self.navigation, job=self.job
        )
