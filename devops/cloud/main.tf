resource "google_storage_bucket" "sage_docs" {
  name                        = "${var.resource_prefix}-sage-docs"
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }
}

output "sage_docs_bucket_name" {
  value = google_storage_bucket.sage_docs.name
}