'use client'

import { useState, useEffect } from 'react'
import AppShell from '@/components/AppShell'
import { FileText, Upload, CheckCircle, XCircle, Clock, Loader2 } from 'lucide-react'
import { documents } from '@/lib/api'

const STATUS_UI = {
  uploaded: {
    label: 'Uploaded',
    className: 'text-blue-600',
    Icon: Clock,
  },
  processing: {
    label: 'Processing',
    className: 'text-amber-600',
    Icon: Loader2,
  },
  verified: {
    label: 'Verified',
    className: 'text-green-600',
    Icon: CheckCircle,
  },
  rejected: {
    label: 'Rejected',
    className: 'text-red-600',
    Icon: XCircle,
  },
}

export default function DocumentsPage() {
  const [documentsList, setDocumentsList] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    try {
      const data = await documents.listMine()
      setDocumentsList(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleUpload = async (e) => {
    e.preventDefault()
    const fileInput = document.getElementById('file-upload')
    if (!fileInput.files.length) return

    setUploading(true)
    setError(null)
    const formData = new FormData()
    formData.append('file', fileInput.files[0])
    const typeInput = document.getElementById('doc-type')
    if (typeInput?.value) {
      formData.append('document_type', typeInput.value)
    }

    try {
      await documents.upload(formData)
      await fetchDocuments()
      fileInput.value = ''
    } catch (err) {
      setError(err.message || 'Failed to upload document')
    } finally {
      setUploading(false)
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">My Documents</h1>

        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Upload New Document</h2>
          <p className="text-sm text-gray-600 dark:text-slate-400 mb-4">
            Accepted types: PDF, JPEG, PNG, WebP, TIFF. The file is stored for admin verification.
          </p>
          {error && <div className="text-red-500 dark:text-red-400 mb-4">{error}</div>}
          <form onSubmit={handleUpload} className="flex flex-col gap-4 max-w-md">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">Document type</label>
              <select
                id="doc-type"
                className="w-full border-gray-300 dark:border-slate-600 rounded-md shadow-sm p-2 border bg-white dark:bg-slate-700 text-gray-900 dark:text-white"
                defaultValue="ID_PROOF"
              >
                <option value="ID_PROOF">ID Proof</option>
                <option value="MARKSHEET_10TH">10th Marksheet</option>
                <option value="MARKSHEET_12TH">12th Marksheet</option>
                <option value="ADDRESS_PROOF">Address Proof</option>
                <option value="PHOTO">Passport Photo</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-slate-300 mb-1">File</label>
              <input
                type="file"
                id="file-upload"
                className="w-full text-gray-900 dark:text-white"
                required
                accept=".pdf,.png,.jpg,.jpeg,.webp,.tiff,.tif"
              />
            </div>
            <button
              type="submit"
              disabled={uploading}
              className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50 transition-colors inline-flex items-center gap-2"
            >
              {uploading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  Upload Document
                </>
              )}
            </button>
          </form>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-gray-100 dark:border-slate-700 p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Uploaded Documents</h2>
          {loading ? (
            <p className="text-gray-500 dark:text-slate-400">Loading documents...</p>
          ) : documentsList.length === 0 ? (
            <p className="text-gray-500 dark:text-slate-400">No documents uploaded yet.</p>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {documentsList.map((doc) => {
                const key = (doc.status || 'uploaded').toLowerCase()
                const ui = STATUS_UI[key] || STATUS_UI.uploaded
                const StatusIcon = ui.Icon
                return (
                  <div
                    key={doc.id}
                    className="border border-gray-200 dark:border-slate-700 rounded-lg p-4 flex flex-col items-center text-center bg-white dark:bg-slate-700"
                  >
                    <FileText className="w-12 h-12 text-indigo-500 mb-2" />
                    <h3 className="font-semibold text-gray-900 dark:text-white px-1">{doc.document_type || 'Document'}</h3>
                    <p className="text-sm text-gray-600 dark:text-slate-400 mb-1 break-all px-1" title={doc.original_filename}>
                      {doc.original_filename}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-slate-500 mb-3">{doc.file_type}</p>

                    <div className="mt-auto pt-2 border-t border-gray-100 dark:border-slate-600 w-full">
                      <span
                        className={`flex items-center justify-center text-sm font-medium gap-1 ${ui.className}`}
                      >
                        <StatusIcon
                          className={`w-4 h-4 ${key === 'processing' ? 'animate-spin' : ''}`}
                        />
                        {ui.label}
                      </span>
                      {doc.status === 'rejected' && doc.rejection_reason && (
                        <p className="text-xs text-red-600 dark:text-red-400 mt-2">{doc.rejection_reason}</p>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </AppShell>
  )
}
