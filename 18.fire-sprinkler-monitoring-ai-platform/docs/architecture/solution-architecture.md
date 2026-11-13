# Solution Architecture

Read-only observations flow from field equipment through a manufacturer-approved gateway into Azure Event Hubs (future cloud ingestion) or the local simulator. ASP.NET Core validates point IDs, derives the configured classification, persists immutable event records and publishes dashboard updates through SignalR. Angular provides operator visibility. Python analyzes historical state patterns and returns advisory insights only.

Future Azure deployment: Angular Static Web Apps/App Service; .NET and Python on Azure Container Apps; Azure Database for PostgreSQL; Event Hubs; Service Bus; Blob Storage; Entra ID; Managed Identity; Key Vault; Azure Monitor and Application Insights.
