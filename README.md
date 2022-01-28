# Plugin Bot

## Warning

This is an example program that uses the Spirit of Korth's Software Development Wrapper for Active Worlds to interact with the [Active Worlds](https://www.activeworlds.com). This project or its contributors are not affiliated with Active Worlds. The Active Worlds SDK is provided in aw64.dll. By using the active worlds SDK, you are agreeing to the terms of the [Active Worlds SDK License Agreement](https://www.activeworlds.com/sdk/download.htm).

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Json Configuration](#json-configuration-file)
  - [User Input](#user-input)
- [Testing](#testing)
- [License](#license)
- [Contribution](#contribution)

## Introduction

The plugin bot handles translating events from an Active Worlds SDK instance into a local event queue. This event queue can then be processed by the plugin. The local event queue can receive events from the plugin or from the Active Worlds SDK. This allows the plugin to be written in a modular fashion, and to be able to create new events for use within other plugins.

The plugin bot automatically dependency injects the event, the bot instance, and any other dependencies into the plugin. The plugin bot will automatically detect plugins that are added and will automatically load them and execute them. The plugin bot will also automatically detect plugins that are removed and will automatically unload them.

## Usage

Inside of a python environment, you can import the requirements and run the following commands to start the project. The plugin bot will automatically load plugins from a directory specified in the configuration. Please refer to the [configuration](#configuration) section for more information.

```bash
pip install -r requirements.txt
python run.py
```

You may also run the project using Docker with the following command.

```bash
docker build --tag plugin .
docker run plugin
```

## Configuration

Configuration is an aggregation of multiple configuration sources. The configuration sources in order of precedence are:

- The environment variables
- The json configuration file
- The user's input

### Environment Variables

    `BOT_NAME`: The name of the bot. This is used to identify the bot in Active Worlds.
    `CITIZEN_NUMBER`: The citizen number for the owner of the bot. This is used to identify which citizen the bot is owned by and which bot count to use.
    `PASSWORD`: The password for the bot. This is used to log the bot into Active Worlds with the citizen number.
    `WORLD_NAME`: The name of the world the bot will enter. This is used to identify which world the bot will enter.
    `WORLD_X`: The x coordinate of the bot. WEST/EAST where WEST is positive and EAST is negative.
    `WORLD_Y`: The y coordinate of the bot. Height where 0 is the ground, positive values are above the ground, and negative values are below the ground.
    `WORLD_Z`: The z coordinate of the bot. NORTH/SOUTH where NORTH is positive and SOUTH is negative.
    'PLUGIN_PATH': The path to the directory containing the plugins.

### Json Configuration File

The json configuration file is a json file that contains the configuration for the bot. The json file must be called `configuration.json`. IF the json file is not found, no errors occur and the configuration is not used.

Configuration example:
```json
{
    "bot_name": "Plugin Bot",
    "world_name": "Test World",
    "world_coordinates": {
        "x": 0,
        "y": 0,
        "z": 0
    },
    "plugin_path": "plugins",
    "citizen_number": 123456,
    "password": "password"
}
```

### User Input

The user input is a series of prompts that are displayed to the user. The user input is used to gather the configuration for the bot when no other configuration is available.

## Testing
To test the library, you can use the `run_tests.py` script.


You may still run the tests on your system, but it is recommended to use the docker image.
```bash
pip install pytest coverage
python run_tests.py
```

## License

This project is licensed under the MIT license.

## Contribution

This project is open source. Feel free to contribute to the project by opening an issue, creating a pull request, or by contacting [Johnny Irvin](mailto:irvinjohnathan@gmail.com). I appreciate any feedback or contributions. This project is not affiliated with Active Worlds, Inc. The creator of this project is not affiliated with Active Worlds, Inc. The Active Worlds SDK is provided in aw64.dll. By using the active worlds SDK, you are agreeing to the terms of the [Active Worlds SDK License Agreement](https://www.activeworlds.com/sdk/download.htm).