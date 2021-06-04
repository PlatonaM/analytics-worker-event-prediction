## analytics-worker-event-prediction

Takes machine learning models trained by [analytics-trainer-event-prediction](https://github.com/PlatonaM/analytics-trainer-event-prediction) and creates predictions based on the provided data window.
Predictions are provided via an HTTP API. To create a prediction first make a job request and then post the data window to start the job.

### Configuration

`CONF_LOGGER_LEVEL`: Set logging level to `info`, `warning`, `error`, `critical` or `debug`.

`CONF_STORAGE_PATH`: Set path for temporary files.

`CONF_STORAGE_CHUNK_SIZE`: Set chunk size.

`CONF_JOBS_MAX_NUM`: Set maximum number of parallel jobs.

`CONF_JOBS_CHECK`: Control how often the trainer checks if new jobs are available.

### Data Structures

#### Job resource

    {
        "id": <string>,
        "created": <string>,
        "status": <string>,
        "data_source": <string>,
        "result": [
            {
                "target": <number>,
                "result": <number>
            }
        ],
        "reason": <string>,
        "sorted_data": <boolean>,
        "models": <object>
    }

#### Job request

    {
        "sorted_data": <boolean>,
        "models": [
            {
                "id": <string>,
                "created": <string>,
                "config": {
                    "sampling_frequency": <string>,
                    "imputations_technique_str": <string>,
                    "imputation_technique_num": <string>,
                    "ts_fresh_window_length": <number>,
                    "ts_fresh_window_end": <number>,
                    "ts_fresh_minimal_features": <boolean>,
                    "balance_ratio": <number>,
                    "random_state": [<number>],
                    "cv": <number>,
                    "oversampling_method": <boolean>,
                    "target_col": <string>,
                    "target_errorCode": <number>,
                    "scaler": <string>,
                    "ml_algorithm": <string>
                }
                "columns": <object>,
                "data": <string>,
                "default_values": <object>,
                "service_id": <string>,
                "time_field": <string>
            }
        ]
    }

### API

#### /jobs

**POST**

_Send a job request to create job resource._

    # Example

    cat new_job_request.json
    {
        "sorted_data": true,
        "models": [
            {
                "id": "def7d53676a6035bd6121bdb72a444fed6aba676cb246d4d2467eb0318574425",
                "created": "2021-05-07T10:21:26.150618Z",
                "config": {
                    "sampling_frequency": "5S",
                    "imputations_technique_str": "pad",
                    "imputation_technique_num": "pad",
                    "ts_fresh_window_length": 30,
                    "ts_fresh_window_end": 30,
                    "ts_fresh_minimal_features": true,
                    "balance_ratio": 0.5,
                    "random_state": [
                        0
                    ],
                    "cv": 5,
                    "oversampling_method": false,
                    "target_col": "module_2_errorcode",
                    "target_errorCode": 1051,
                    "scaler": "StandardScaler",
                    "ml_algorithm": "RandomForestClassifier"
                },
                "columns": [
                    "time",
                    "location_ec-generator_gesamtwirkleistung",
                    "location_ec-gesamt_gesamtwirkleistung",
                    "location_ec-prozess_gesamtwirkleistung",
                    "location_ec-roboter_gesamtwirkleistung",
                    "location_roboter-ausgabe_gesamtwirkleistung",
                    "location_roboter-eingabe_gesamtwirkleistung",
                    "location_transport-gesamt_gesamtwirkleistung",
                    "location_wm1-gesamt_gesamtwirkleistung",
                    "location_wm1-heizung-reinigen_gesamtwirkleistung",
                    "location_wm1-heizung-trocknung_gesamtwirkleistung",
                    "location_wm2-gesamt_gesamtwirkleistung",
                    "location_wm2-heizung-reinigen_gesamtwirkleistung",
                    "location_wm2-heizung-trocknung_gesamtwirkleistung",
                    "location_wm2-vakuumpumpe_gesamtwirkleistung",
                    "module_1_errorcode",
                    "module_1_errorindex",
                    "module_1_state",
                    "module_1_station_1_process_1_errorcode_0",
                    "module_1_station_1_process_1_errorcode_980",
                    "module_1_station_2_process_1_errorcode_0",
                    "module_1_station_2_process_1_errorcode_980",
                    "module_1_station_31_process_1_errorcode_0",
                    "module_1_station_31_process_1_errorcode_980",
                    "module_1_station_31_process_1_errorcode_998",
                    "module_1_station_3_process_1_errorcode_0",
                    "module_1_station_3_process_1_errorcode_980",
                    "module_1_station_4_process_1_errorcode_0",
                    "module_1_station_4_process_1_errorcode_980",
                    "module_1_station_5_process_1_errorcode_0",
                    "module_1_station_5_process_1_errorcode_980",
                    "module_1_station_6_process_1_errorcode_0",
                    "module_1_station_6_process_1_errorcode_980",
                    "module_2_errorcode",
                    "module_2_errorindex",
                    "module_2_state",
                    "module_2_station_1_process_1_errorcode_0",
                    "module_2_station_21_process_1_errorcode_999",
                    "module_2_station_22_process_1_errorcode_0",
                    "module_2_station_22_process_1_errorcode_999",
                    "module_2_station_24_process_1_errorcode_0",
                    "module_2_station_25_process_1_errorcode_51",
                    "module_2_station_25_process_1_errorcode_53",
                    "module_2_station_25_process_1_errorcode_55",
                    "module_2_station_28_process_1_errorcode_51",
                    "module_2_station_28_process_1_errorcode_53",
                    "module_2_station_28_process_1_errorcode_55",
                    "module_2_station_28_process_1_errorcode_980",
                    "module_2_station_29_process_1_errorcode_0",
                    "module_2_station_3_process_1_errorcode_0",
                    "module_2_station_3_process_1_errorcode_998",
                    "module_2_station_4_process_1_errorcode_0",
                    "module_2_station_4_process_1_errorcode_998",
                    "module_2_station_50_process_1_errorcode_0",
                    "module_2_station_51_process_1_errorcode_0",
                    "module_2_station_51_process_1_errorcode_51",
                    "module_2_station_51_process_1_errorcode_53",
                    "module_2_station_51_process_1_errorcode_55",
                    "module_2_station_5_process_1_errorcode_0",
                    "module_2_station_5_process_1_errorcode_998",
                    "module_2_station_6_process_1_errorcode_0",
                    "module_2_station_6_process_1_errorcode_998",
                    "module_4_errorcode",
                    "module_4_errorindex",
                    "module_4_state",
                    "module_5_errorcode",
                    "module_5_errorindex",
                    "module_5_state",
                    "module_6_errorcode",
                    "module_6_errorindex",
                    "module_6_state"
                ],
                "data": "H4sIAKYUlWAC/+Vde0BU1dYf3sNDGBUVj....",
                "default_values": {
                    "module_2_station_4_process_1_errorcode_0": 0,
                    "module_1_station_1_process_1_errorcode_0": 0,
                    "module_2_station_51_process_1_errorcode_0": 0,
                    "module_2_station_3_process_1_errorcode_0": 0,
                    "module_2_station_50_process_1_errorcode_0": 0,
                    "module_2_station_24_process_1_errorcode_0": 0,
                    "module_2_station_5_process_1_errorcode_0": 0,
                    "module_1_station_31_process_1_errorcode_0": 0,
                    "module_1_station_5_process_1_errorcode_0": 0,
                    "module_1_station_2_process_1_errorcode_0": 0,
                    "module_1_station_3_process_1_errorcode_0": 0,
                    "module_1_station_6_process_1_errorcode_0": 0,
                    "module_1_station_4_process_1_errorcode_0": 0,
                    "module_2_station_6_process_1_errorcode_0": 0,
                    "module_2_station_22_process_1_errorcode_0": 0,
                    "module_2_station_21_process_1_errorcode_999": 0,
                    "module_2_station_1_process_1_errorcode_0": 0,
                    "module_2_station_4_process_1_errorcode_998": 0,
                    "module_2_station_3_process_1_errorcode_998": 0,
                    "module_2_station_5_process_1_errorcode_998": 0,
                    "module_2_station_6_process_1_errorcode_998": 0,
                    "module_1_station_31_process_1_errorcode_998": 0,
                    "module_2_station_51_process_1_errorcode_51": 0,
                    "module_2_station_25_process_1_errorcode_51": 0,
                    "module_2_station_51_process_1_errorcode_55": 0,
                    "module_2_station_25_process_1_errorcode_55": 0,
                    "module_2_station_28_process_1_errorcode_55": 0,
                    "module_2_station_28_process_1_errorcode_51": 0,
                    "module_2_station_28_process_1_errorcode_980": 0,
                    "module_2_station_51_process_1_errorcode_53": 0,
                    "module_2_station_25_process_1_errorcode_53": 0,
                    "module_2_station_28_process_1_errorcode_53": 0,
                    "module_2_station_29_process_1_errorcode_0": 0,
                    "module_2_station_22_process_1_errorcode_999": 0,
                    "module_1_station_1_process_1_errorcode_980": 0,
                    "module_1_station_31_process_1_errorcode_980": 0,
                    "module_1_station_5_process_1_errorcode_980": 0,
                    "module_1_station_3_process_1_errorcode_980": 0,
                    "module_1_station_2_process_1_errorcode_980": 0,
                    "module_1_station_6_process_1_errorcode_980": 0,
                    "module_1_station_4_process_1_errorcode_980": 0
                },
                "service_id": "urn:infai:ses:service:c2872437-3e53-49c6-a5be-bf264d52430d",
                "time_field": "time"
            }
        ]
    }

    curl \
    -d @new_job_request.json \
    -H `Content-Type: application/json` \
    -X POST http://<host>/models

    # Response with job ID as text
    851d15e002da49b2956289b32828fb30

#### /jobs/{job}

**GET**

_Retrieve a job resource._

    # Example    

    # With no data
    curl http://<host>/jobs/851d15e002da49b2956289b32828fb30
    {
        "id": "851d15e002da49b2956289b32828fb30",
        "created": "2021-05-07T10:21:26.150618Z",
        "status": "nodata",
        "data_source": null,
        "result": null,
        "reason": null,
        "sorted_data": true,
        "models": [
            "def7d53676a6035bd6121bdb72a444fed6aba676cb246d4d2467eb0318574425"
        ]
    }

    # With data and result
    curl http://<host>/jobs/851d15e002da49b2956289b32828fb30
    {
        "id": "851d15e002da49b2956289b32828fb30",
        "created": "2021-05-07T10:21:26.150618Z",
        "status": "finished",
        "data_source": 7961b70dbc6b4059adcd4a5f4919fa8c,
        "result": [
            {
                "target": 1051,
                "result": 0
            }
        ],
        "reason": null,
        "sorted_data": true,
        "models": [
            "def7d53676a6035bd6121bdb72a444fed6aba676cb246d4d2467eb0318574425"
        ]
    }

**POST**

_Add data to a job and enqueue it for execution._

    # Example

    curl --data-binary @data_window http://<host>/jobs/851d15e002da49b2956289b32828fb30
