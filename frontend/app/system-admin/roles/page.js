'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Key, Shield } from 'lucide-react'

export default function SysAdminRoles() {
  const roles = [
    { name: 'student', description: 'Default role for admission applicants and students', users: 245, system: false },
    { name: 'admin', description: 'Handles admission operations and document verification', users: 8, system: false },
    { name: 'mentor', description: 'Faculty mentor guiding assigned students', users: 25, system: false },
    { name: 'department_coordinator', description: 'Department-level admission coordination', users: 6, system: false },
    { name: 'system_admin', description: 'Full platform administration and configuration', users: 2, system: true },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Roles & Permissions</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Manage RBAC configuration</p>
        </div>
        <Button size="sm" variant="outline"><Shield className="w-4 h-4 mr-1" /> Seed Permissions</Button>
      </div>

      <Card>
        <CardHeader><CardTitle>All Roles</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-3">
            {roles.map((r) => (
              <div key={r.name} className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-3">
                  <Key className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white capitalize">{r.name.replace('_', ' ')}</p>
                    <p className="text-xs text-slate-500">{r.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-500">{r.users} users</span>
                  {r.system && <Badge variant="destructive" className="text-[10px]">System</Badge>}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
