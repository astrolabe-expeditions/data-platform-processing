# Architecture

## Database

This database schema is deliberately simplified. It does not include user management concepts.

```mermaid

erDiagram
    stations {
        String test
        String id
        String name
        StationType type
        String latitude
        String longitude
        String description
        String image_url
    }

    sensors {
        _id String
        identifier String
        type SensorType
        nbr_measures   Int
        station_id String
        created_at      DateTime
        updated_at      DateTime
        deleted_at      DateTime

    }

    records {
        _id String
        id                  String
        latitude            String
        longitude           String
        recorded_at         DateTime
        battery_voltage     Float
        battery_percentage  Float
        pression_ext        Float
        temp_ext            Float
        temp_int            Float
        temp_sea            Float[]
        temp_sea_mean       Float
        ec_sea              Float[]
        ec_sea_mean         Float
        depth               Float[]
        depth_mean          Float
        sensor_id           String
        created_at          DateTime
        updated_at          DateTime
        deleted_at          DateTime
         }

    files {
        _id String
        name            String
        status          String
        file_url        String
        sensor_id       String
        created_at      DateTime
        updated_at      DateTime
        deleted_at      DateTime
    }

    stations ||--|{ sensors : has
    sensors ||--o{ records : contains
    sensors ||--o{ files : contains
```

## Interacting with the interface

```mermaid
sequenceDiagram
    Web app->>+S3: Upload file
    Web app->>+Cloud function: Call with the id of the file to process
    Cloud function->>+Database: Get the file data and put status to process
    Cloud function->>+S3: Get the CSV file
    Cloud function->>+Cloud function: Processing the file
    Cloud function->>+Database: Upload data into records with sensor_id corresponding
    Cloud function->>+Database: Set file status processed
```