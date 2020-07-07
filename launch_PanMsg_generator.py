# Generic import
import json
import random
import multiprocessing
import time

#Local utils
from utils.messaging import PanMessaging

#msg_subscriber = PanMessaging.create_subscriber(6511)
def create_forwarder(port):
    try:
        PanMessaging.create_forwarder(port, port + 1)
    except Exception:
        pass

msg_forwarder_process = multiprocessing.Process(
    target=create_forwarder, args=(
        6510,), name='MsgForwarder')
msg_forwarder_process.start()
msg_publisher = PanMessaging.create_publisher(6510)

sample_msgs = [
[
    "STATUS",
    {
        "observatory": {
            "mount": {
                "current_dec": 55.118,
                "current_ha": 1.021,
                "current_ra": 15.314,
                "guide_rate_ns": 0.5,
                "guide_rate_we": 0.5,
                "slew_rate": "3x",
                "track_mode": "TRACK_SIDEREAL"
            },
            "observatory": {
                "altitude": 150.0,
                "dome": {
                    "is_open": True
                },
                "location": {
                    "latitude": 43.56,
                    "longitude": 5.43
                },
                "owner": "gnthibault",
                "scope": {
                    "camera_relay": False,
                    "corrector_dew": False,
                    "finder_dew": False,
                    "finder_dustcap_open": True,
                    "flat_panel": False,
                    "mount_relay": False,
                    "scope_dew": False,
                    "scope_dustcap_open": True,
                    "scope_fan": False
                },
                "timezone": "Europe/Paris"
            },
            "observer": {
                "local_evening_astro_time": "21:39:50",
                "local_moon_alt": -48.592,
                "local_moon_illumination": 0.93,
                "local_moon_phase": 0.535,
                "local_morning_astro_time": "01:47:02",
                "local_sun_rise_time": "04:09:51",
                "local_sun_set_time": "19:17:06",
                "localtime": "2020-07-07 18:40:03.519329+02:00",
                "siderealtime": "12h06m11.7216s",
                "utctime": "2020-07-07 16:40:03"
            },
            "scheduler": None
        },
        "state": "scheduling",
        "system": {
            "free_space": 145.688
        }
    }
],
[
    "PANCHAT",
    {
        "message": "Ok, I'm finding something good to look at...",
        "timestamp": "2020-07-07 16:40:04"
    }
],
[
    "PANCHAT",
    {
        "message": "No valid observations found. Cannot schedule. Going to park.",
        "timestamp": "2020-07-07 16:40:04"
    }
],
[
    "STATUS",
    {
        "observatory": {
            "mount": {
                "current_dec": 55.118,
                "current_ha": 1.021,
                "current_ra": 15.314,
                "guide_rate_ns": 0.5,
                "guide_rate_we": 0.5,
                "slew_rate": "3x",
                "track_mode": "TRACK_SIDEREAL"
            },
            "observatory": {
                "altitude": 150.0,
                "dome": {
                    "is_open": True
                },
                "location": {
                    "latitude": 43.56,
                    "longitude": 5.43
                },
                "owner": "gnthibault",
                "scope": {
                    "camera_relay": False,
                    "corrector_dew": False,
                    "finder_dew": False,
                    "finder_dustcap_open": True,
                    "flat_panel": False,
                    "mount_relay": False,
                    "scope_dew": False,
                    "scope_dustcap_open": True,
                    "scope_fan": False
                },
                "timezone": "Europe/Paris"
            },
            "observer": {
                "local_evening_astro_time": "21:39:50",
                "local_moon_alt": -48.589,
                "local_moon_illumination": 0.93,
                "local_moon_phase": 0.535,
                "local_morning_astro_time": "01:47:02",
                "local_sun_rise_time": "04:09:51",
                "local_sun_set_time": "19:17:05",
                "localtime": "2020-07-07 18:40:04.526112+02:00",
                "siderealtime": "12h06m12.6691s",
                "utctime": "2020-07-07 16:40:04"
            },
            "scheduler": None
        },
        "state": "parking",
        "system": {
            "free_space": 145.688
        }
    }
],
[
    "PANCHAT",
    {
        "message": "Taking it on home and then parking.",
        "timestamp": "2020-07-07 16:40:05"
    }
],
[
    "WEATHER",
    {
        "data": {
            "WEATHER_FORECAST": 0.0,
            "WEATHER_RAIN_HOUR": 0.0,
            "WEATHER_TEMPERATURE": 15.0,
            "WEATHER_WIND_GUST": 0.0,
            "WEATHER_WIND_SPEED": 10.0,
            "date": "2020-07-07T16:40:30.742775+00:00",
            "safe": True,
            "state": "OK",
            "weather_sensor_name": "Weather Simulator"
        }
    }
],
[
    "STATUS",
    {
        "observatory": {
            "mount": {
                "current_dec": 0.0,
                "current_ha": 24.0,
                "current_ra": 360.0,
                "guide_rate_ns": 0.5,
                "guide_rate_we": 0.5,
                "slew_rate": "3x",
                "track_mode": "TRACK_SIDEREAL"
            },
            "observatory": {
                "altitude": 150.0,
                "dome": {
                    "is_open": False
                },
                "location": {
                    "latitude": 43.56,
                    "longitude": 5.43
                },
                "owner": "gnthibault",
                "scope": {
                    "camera_relay": False,
                    "corrector_dew": False,
                    "finder_dew": False,
                    "finder_dustcap_open": False,
                    "flat_panel": False,
                    "mount_relay": False,
                    "scope_dew": False,
                    "scope_dustcap_open": False,
                    "scope_fan": False
                },
                "timezone": "Europe/Paris"
            },
            "observer": {
                "local_evening_astro_time": "21:39:50",
                "local_moon_alt": -48.511,
                "local_moon_illumination": 0.93,
                "local_moon_phase": 0.535,
                "local_morning_astro_time": "01:47:02",
                "local_sun_rise_time": "04:09:51",
                "local_sun_set_time": "19:17:05",
                "localtime": "2020-07-07 18:40:33.414082+02:00",
                "siderealtime": "12h06m41.67s",
                "utctime": "2020-07-07 16:40:33"
            },
            "scheduler": None
        },
        "state": "parked",
        "system": {
            "free_space": 145.688
        }
    }
],
[
    "PANCHAT",
    {
        "message": "No observations found.",
        "timestamp": "2020-07-07 16:40:34"
    }
],
[
    "PANCHAT",
    {
        "message": "Going to stay parked for half an hour then will try again.",
        "timestamp": "2020-07-07 16:40:34"
    }
],
[
    "STATUS",
    {
        "observatory": {
            "mount": {
                "current_dec": 0.0,
                "current_ha": 24.0,
                "current_ra": 360.0,
                "guide_rate_ns": 0.5,
                "guide_rate_we": 0.5,
                "slew_rate": "3x",
                "track_mode": "TRACK_SIDEREAL"
            },
            "observatory": {
                "altitude": 150.0,
                "dome": {
                    "is_open": False
                },
                "location": {
                    "latitude": 43.56,
                    "longitude": 5.43
                },
                "owner": "gnthibault",
                "scope": {
                    "camera_relay": False,
                    "corrector_dew": False,
                    "finder_dew": False,
                    "finder_dustcap_open": False,
                    "flat_panel": False,
                    "mount_relay": False,
                    "scope_dew": False,
                    "scope_dustcap_open": False,
                    "scope_fan": False
                },
                "timezone": "Europe/Paris"
            },
            "observer": {
                "local_evening_astro_time": "21:39:50",
                "local_moon_alt": -48.509,
                "local_moon_illumination": 0.93,
                "local_moon_phase": 0.535,
                "local_morning_astro_time": "01:47:02",
                "local_sun_rise_time": "04:09:51",
                "local_sun_set_time": "19:17:05",
                "localtime": "2020-07-07 18:40:34.260980+02:00",
                "siderealtime": "12h06m42.4857s",
                "utctime": "2020-07-07 16:40:34"
            },
            "scheduler": None
        },
        "state": "parked",
        "system": {
            "free_space": 145.688
        }
    }
],
[
    "WEATHER",
    {
        "data": {
            "WEATHER_FORECAST": 0.0,
            "WEATHER_RAIN_HOUR": 0.0,
            "WEATHER_TEMPERATURE": 15.0,
            "WEATHER_WIND_GUST": 0.0,
            "WEATHER_WIND_SPEED": 10.0,
            "date": "2020-07-07T16:41:30.816454+00:00",
            "safe": True,
            "state": "OK",
            "weather_sensor_name": "Weather Simulator"
        }
    }
]]


while True:
  #msg = msg_subscriber.receive_message()
  #print(json.dumps(msg, indent=4, sort_keys=True))
  channel, msg = random.choice(sample_msgs)
  msg_publisher.send_message(channel, msg)
  time.sleep(4)

#launch with PYTHONPATH=. python3 ../PAWS/launch_PanMsg_generator.py
