CREATE TABLE IF NOT EXISTS "tests" (
    "measurement_id" TEXT NOT NULL PRIMARY KEY, --A waveform's unique identifier
    "test_id" TEXT NOT NULL, -- A test scan's unique identifier
    "project_name" TEXT, --The name of the project that a scan belongs under
    "timestamp" DATETIME NOT NULL, --timestamp a scan was taken at
    "exp_group" TEXT, --More project information that a scan belongs under
    "serial_number" TEXT, --Serial number of the a scan was taken on
    "sample_state" TEXT, --Text information about the sample the scan was taken on
    "n_rows" INTEGER, -- Number of rows in a scan
    "n_columns" INTEGER, --Number of columns in a scan
    "row_spacing" REAL, --Physical spacing between row points
    "col_spacing" REAL, --Physical spacing between column points
    "score" REAL, --A scan's score
    "sample_rate" INTEGER NOT NULL, --Sample rate of the waveform
    "duration" REAL NOT NULL, --The duration of a waveform was taken at
    "delay" REAL NOT NULL, -- The delay on a waveform's data read
    "position_x" INTEGER, --A wave's X index in the scan
    "position_y" INTEGER, --A wave's Y index in the scan
    "data" ARRAY NOT NULL --Waveform data
);

CREATE INDEX "tests_test_id" ON "tests" ("test_id");

CREATE INDEX "tests_timestamp" ON "tests" ("timestamp");