'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Search, Shield } from 'lucide-react'

export default function SysAdminAudit() {
  const logs = [
    { user: 'admin@college.ac.in', action: 'User Login', resource: 'Auth', details: 'Successful login from 192.168.1.1', time: '2026-05-14 14:32:00', status: 'success' },
    { user: 'system', action: 'Role Update', resource: 'RBAC', details: 'Permission updated for admin role', time: '2026-05-14 13:15:00', status: 'success' },
    { user: 'coordinator@college.ac.in', action: 'Document Verify', resource: 'Documents', details: 'Document #1024 verified', time: '2026-05-14 12:00:00', status: 'success' },
    { user: 'unknown', action: 'Failed Login', resource: 'Auth', details: 'Invalid credentials for admin@college.ac.in', time: '2026-05-14 11:45:00', status: 'error' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Audit Logs</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Track all system actions for compliance</p>
        </div>
        <Badge variant="destructive">Restricted</Badge>
      </div>

      <div className="relative max-w-sm">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <Input placeholder="Search audit logs..." className="pl-9" />
      </div>

      <Card>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-slate-50 dark:bg-slate-800/50">
                  <th className="text-left py-3 px-4 font-medium text-slate-500">User</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Action</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Resource</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Details</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Time</th>
                  <th className="text-left py-3 px-4 font-medium text-slate-500">Status</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, i) => (
                  <tr key={i} className="border-b border-slate-100 dark:border-slate-800">
                    <td className="py-3 px-4 text-slate-900 dark:text-white">{log.user}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{log.action}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400">{log.resource}</td>
                    <td className="py-3 px-4 text-slate-600 dark:text-slate-400 max-w-xs truncate">{log.details}</td>
                    <td className="py-3 px-4 text-slate-500 text-xs">{log.time}</td>
                    <td className="py-3 px-4">
                      <Badge variant={log.status === 'success' ? 'success' : 'destructive'} className="text-[10px]">{log.status}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
