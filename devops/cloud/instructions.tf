# Bucket con le istruzioni aggiuntive di Sage (istruzioni.md).
resource "google_storage_bucket" "instructions" {
  project                     = var.project_id
  name                        = "${var.resource_prefix}-instructions"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [google_project_service.apis]
}

# Il service account di Cloud Run può solo leggere i file del bucket.
resource "google_storage_bucket_iam_member" "sage_run_instructions" {
  bucket = google_storage_bucket.instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
}
