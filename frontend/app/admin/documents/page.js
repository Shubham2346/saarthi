'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function AdminDocuments() {
  const [pendingDocs, setPendingDocs] = useState([])
  const [loading, setLoading] = useState(true)

  const loadDocs = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/documents/pending`, { headers: { Authorization: `Bearer ${token}` } })
      if (res.ok) setPendingDocs(await res.json())
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => { loadDocs() }, [])

  const handleVerify = async (docId, status) => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/documents/${docId}/verify`, {
        method: 'PATCH',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
      })
      if (res.ok) loadDocs()
    } catch (e) { console.error(e) }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Document Verification</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Verify student uploaded documents</p>
        </div>
        <Badge variant="warning">{pendingDocs.length} pending</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Pending Documents</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50">
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Document Type</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">File Name</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">User</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Status</th>
                  <th className="text-right py-3 px-4 font-medium text-slate-500">Actions</th>
                </tr>
              </thead>
              <tbody>
                {pendingDocs.map((doc) => (
                  <tr key={doc.id} className="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <td className="py-3 px-4 text-slate-900 dark:text-white capitalize">{doc.document_type?.replace('_', ' ') || '-'}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{doc.original_filename || doc.filename}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{doc.user_email || doc.user_id?.slice(0, 8)}</td>
                    <td className="py-3 px-4">
                      <Badge variant="warning">{doc.status || 'pending'}</Badge>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex justify-end gap-2">
                        <Button size="sm" variant="outline" className="text-emerald-600 border-emerald-200 hover:bg-emerald-50" onClick={() => handleVerify(doc.id, 'verified')}>
                          Approve
                        </Button>
                        <Button size="sm" variant="outline" className="text-red-600 border-red-200 hover:bg-red-50" onClick={() => handleVerify(doc.id, 'rejected')}>
                          Reject
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
                {pendingDocs.length === 0 && (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-slate-500">No pending documents</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
