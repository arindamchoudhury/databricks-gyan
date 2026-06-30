# Subscribe to Google Pub/Sub

> **Source:** [docs.databricks.com/aws/en/connect/streaming/pub-sub](https://docs.databricks.com/aws/en/connect/streaming/pub-sub)
> **Added:** 2026-06-30
> **Source updated:** 2026-06-18
> **Tags:** structured-streaming, pub-sub, google-cloud, streaming-source, I2
> **Type:** documentation

Built-in connector for reading from Google Pub/Sub as a Structured Streaming source. Format: `"pubsub"`.

**Exactly-once** semantics from the connector. But: Pub/Sub itself may publish duplicate rows or deliver rows out of order — code must handle both.

## Configure a stream

Required options: `subscriptionId`, `topicId`, `projectId` + auth options. Use Databricks secrets for credentials.

```python
auth_options = {
    "clientId": client_id,
    "clientEmail": client_email,
    "privateKey": private_key,
    "privateKeyId": private_key_id
}

query = (spark.readStream
    .format("pubsub")
    .option("subscriptionId", "mysub")
    .option("topicId", "mytopic")
    .option("projectId", "myproject")
    .options(auth_options)
    .load()
)
```

SQL (Lakeflow Declarative Pipelines):

```sql
CREATE OR REFRESH STREAMING TABLE pubsub_raw
AS SELECT * FROM STREAM read_pubsub(
  subscriptionId => 'mysub',
  projectId => 'myproject',
  topicId => 'mytopic',
  clientEmail => secret('pubsub-scope', 'clientEmail'),
  clientId => secret('pubsub-scope', 'clientId'),
  privateKeyId => secret('pubsub-scope', 'privateKeyId'),
  privateKey => secret('pubsub-scope', 'privateKey')
);
```

## GCP IAM roles

| Role | Required? | Purpose |
|---|---|---|
| `roles/pubsub.viewer` or `roles/viewer` | Required | Check subscription exists |
| `roles/pubsub.subscriber` | Required | Fetch data from subscription |
| `roles/pubsub.editor` or `roles/editor` | Optional | Create subscription if missing; `deleteSubscriptionOnStreamStop` |

**Gotcha:** if required roles are granted at resource level (not project level), apply both roles to both the topic **and** the subscription — granting only on the topic is insufficient.

## Schema

| Field | Type |
|---|---|
| `messageId` | `StringType` |
| `payload` | `ArrayType[ByteType]` |
| `attributes` | `StringType` |
| `publishTimestampInMillis` | `LongType` |

## Incremental batch processing

`Trigger.AvailableNow` is supported. Records the timestamp at read start; batch includes all previously fetched data + newly published rows with timestamp < start timestamp.

## Metrics

```json
{
  "numDuplicatesSinceStreamStart": "1",
  "numRecordsReadyToProcess": "1",
  "sizeOfRecordsReadyToProcess": "8"
}
```

## Limitations

Pub/Sub does not support speculative execution (`spark.speculation`).

[[structured-streaming-delta-lake]] · [[structured-streaming-foreach]]
