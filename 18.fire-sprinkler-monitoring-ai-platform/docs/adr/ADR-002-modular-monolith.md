# ADR-002: Modular monolith
Status: Accepted for MVP. Use one ASP.NET Core API plus a separate Python analytics service. This limits distributed complexity during the four-week build; extract services when measured scaling or team ownership justifies it.
