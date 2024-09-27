
# my-housekeeper

`housekeeper` is a Python command-line utility for managing various daily operations, including accounting, locking, recording meals, scheduling, and encouraging yourself.

## Usage

```bash
housekeeper [-h] {accountant,locker,feeder,encourager,scheduler} ...
```

### Subcommands

- `accountant`: Add, update, list, delete transactions.
- `locker`: Add, update, get, delete credentials.
- `feeder`: Add, update, list, delete meals.
- `encourager`: Interact with AI encourager.
- `scheduler`: Add, complete, list, delete tasks.

### General Options

- `-h, --help`: Show the help message and exit.
- See help for more.

## Installation

### 1. Clone the Repository

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/7angel4/my-housekeeper.git
cd housekeeper
```

### 2. Install the Package

You can install the package using `pip`:

```bash
pip install .
```

This will allow you to use the `housekeeper` command from anywhere on your system.

## Examples

### Show Help

To display help information for the `housekeeper` command:

```bash
housekeeper -h
```

To display help information for the `scheduler` subcommand:
```bash
housekeeper scheduler -h
```
or
```bash
housekeeper scheduler --help
```

To add a new task "download my-housekeeper" on April 15, 2024, with estimated duration 0.000001 hrs, using the scheduler:
```bash
housekeeper scheduler add -d 2024-04-15 -t "download my-housekeeper" -du 0.000001
```
You should then see this response: `Added task on 2024-04-15.`

## Contributing

Feel free to open issues or submit pull requests if you want to improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
