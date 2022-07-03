### Files
- `README.md` - This file
- `hiring_test.db` - An SQLite3 database file
- `hiring_test.py` - A script that includes a class for interacting with the above database, and some examples of using that class
- `schema.sql` - Schema information about the database
- `requirements.txt` - Dependency information

### Background
The basic output of the measurements we perform at Feasible is the acoustic waveform, represented as amplitude (voltage) values over a period of time.

Acoustic waveforms are represented digitally as 1-dimensional arrays of amplitude values, together with a few values (eg. sample rate) needed to reproduce the waveform's time axis. A typical array length is in the tens of thousands, and would represent a waveform 10-100 microseconds long. The software often manipulates thousands of waveforms at a time.


When we take a scan of a sample, it is stored in an SQLite3 database using the schema shown below. One scan of a sample can be identified by a universally unique ID, `test_id`, and is composed of multiple waveforms. Each waveform is identified by an ID string `measurement_id` and the unixtime of its creation, `timestamp`. Stored alongside are a number of metadata and spatial properties that describe the who/what/why/where/how of the measurement. 

### The Problem
We are attempting to build a `class` that handles the uploading of the collected data. Before we can do that, you are tasked to build out must read the data from the database and manipulate it in such a way that minimizes redundancy and memory utilization while still being easy to handle.

Given `hiring_test.py`, you start with a minimal class `LocalDB` to interact with the sample database `hiring_test.db`. `LocalDB` needs to be extended to make it easier to access the data programmatically.

### Your Tasks:
1. Design a data structure and **any supporting documentation** such that it:
    - Contains all of the information of a single scan, **including its constituent waveforms**
    - Minimizes redundant data fields.
    - Is easily extendable to allow for potentially new fields.
    - Is understandable by other programmers.
    - Can be passed into a method for data upload or manipulation.
        - This does not restrict you to `JSON` or any standard Python data structures. 

2. Modify the `LocalDB` class, refactoring if desired, to add the following methods.
    - `fetch_data(**kwargs)`
        - Potential `kwargs` options that the method should handle:
            - `serial_number: str` Return data where `tests.serial_number` is equal to this value
            - `project_name: str` Return data where `tests.project_name` is equal to this value
            - `before: float` Only return values with `timestamp` below (before) this value.
            - `after: float` Only return values with `timestamp` above (after) this value.
            - `limit: int` Return at most this many entries
        - `fetch_data` should output a ***stream or collection of your data structures***
    - `test_counts(): -> list`
        - This method will return a `list` where each element is a tuple of two elements:
            - A distinct `project_name`
            - A count of `test_id`s that fall under that project.

3. Having done that, what do you see that could be improved in the future, and what issues might arise as the class is integrated and built upon? You can answer in the form of method stubs, comments in your code, a `TODO.md` file, or similar. The goal is not to be exhaustive or highly-detailed, but rather to assess what exists and identify future features and optimizations that could be added to a roadmap.

### Additional Notes

- Feel free to use other non-standard libraries if desired. If you do, update the `requirements.txt` file.
- You should limit the time you spend on this assessment to 1-2 hours.
- Our goals in this assessment are to better understand:
    - your thought and decision processes as you solve a real problem
    - your practical knowledge and comfort with the tools
    - the quality of what you can produce
- Be prepared to discuss your approach and design decisions.