# Database Firestore (uno per persona, chiamato come il prefisso).
resource "google_firestore_database" "sage" {
  project     = var.project_id
  name        = var.resource_prefix
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.apis]
}

# Indice vettoriale sul campo "embedding" (768 dimensioni, come embedding_dimension).
resource "google_firestore_index" "chunks_embedding" {
  project     = var.project_id
  database    = google_firestore_database.sage.name
  collection  = "chunks"
  query_scope = "COLLECTION"

  fields {
    field_path = "embedding"
    vector_config {
      dimension = 768
      flat {}
    }
  }
}

# Il service account di Cloud Run può leggere e scrivere su Firestore.
resource "google_project_iam_member" "sage_run_firestore" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.sage_run.email}"
}
