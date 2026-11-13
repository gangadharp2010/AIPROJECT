resource "azurerm_resource_group" "main" { name="rg-${var.project_name}-${var.environment}" location=var.location tags={project=var.project_name environment=var.environment purpose="portfolio-demo"} }
output "resource_group_name" { value=azurerm_resource_group.main.name }
