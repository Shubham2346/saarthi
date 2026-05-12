'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { documents } from '@/lib/api'
import styles from './page.module.css'

export default function DocumentsPage() {
  const [docs, setDocs] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [file, setFile] = useState(null)

  useEffect(() => {
    fetchDocuments()
  }, [])

  async function fetchDocuments() {
    try {
      const data = await documents.listMy()
      setDocs(data)
    } catch (err) {
      console.error('Failed to load documents', err)
    } finally {
      setLoading(false)
    }
  }

  async function handleUpload(e) {
    e.preventDefault()
    if (!file) return

    setUploading(true)
    try {
      await documents.upload(file)
      setFile(null)
      fetchDocuments() // Refresh the list
    } catch (err) {
      console.error('Upload failed', err)
      alert('Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'verified': return <span className="badge badge-success">Verified</span>
      case 'rejected': return <span className="badge badge-error">Rejected</span>
      case 'processing': return <span className="badge badge-info">Processing</span>
      default: return <span className="badge badge-warning">Uploaded</span>
    }
  }

  return (
    <AppShell>
      <div className={styles.page}>
        <div className={styles.header}>
          <div>
            <h1 className={styles.title}>My Documents</h1>
            <p className={styles.subtitle}>Upload and track your verification documents.</p>
          </div>
        </div>

        <div className={styles.grid}>
          {/* Upload Section */}
          <div className={`card ${styles.uploadCard}`}>
            <h2>Upload Document</h2>
            <form onSubmit={handleUpload} className={styles.uploadForm}>
              <div className={styles.fileInput}>
                <input 
                  type="file" 
                  accept="image/*,application/pdf"
                  onChange={(e) => setFile(e.target.files[0])}
                  disabled={uploading}
                />
              </div>
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={!file || uploading}
              >
                {uploading ? 'Uploading...' : 'Upload'}
              </button>
            </form>
            <p className={styles.hint}>Supported formats: JPG, PNG, PDF (Max 5MB)</p>
          </div>

          {/* List Section */}
          <div className={styles.docList}>
            <h2>Uploaded Documents</h2>
            {loading ? (
              <div className="skeleton" style={{ height: 100, borderRadius: 12 }}></div>
            ) : docs.length === 0 ? (
              <div className={styles.emptyState}>
                <p>No documents uploaded yet.</p>
              </div>
            ) : (
              <div className={styles.list}>
                {docs.map(doc => (
                  <div key={doc.id} className={`card ${styles.docCard}`}>
                    <div className={styles.docInfo}>
                      <span className={styles.docIcon}>📄</span>
                      <div>
                        <h3>{doc.original_filename}</h3>
                        <p>Uploaded: {new Date(doc.created_at).toLocaleDateString()}</p>
                      </div>
                    </div>
                    <div className={styles.docStatus}>
                      {getStatusBadge(doc.status)}
                      {doc.status === 'rejected' && (
                        <p className={styles.rejectionReason}>{doc.rejection_reason}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </AppShell>
  )
}
