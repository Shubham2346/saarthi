'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Settings, Save } from 'lucide-react'

export default function SysAdminSettings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">System Settings</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Configure platform settings</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>General</CardTitle>
            <CardDescription>Basic platform configuration</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {[
              { label: 'Platform Name', value: 'Saarthi' },
              { label: 'Support Email', value: 'support@saarthi.dev' },
              { label: 'Max Upload Size (MB)', value: '10' },
              { label: 'Session Timeout (mins)', value: '60' },
            ].map((s) => (
              <div key={s.label}>
                <label className="text-sm font-medium text-slate-700 dark:text-slate-300">{s.label}</label>
                <Input defaultValue={s.value} className="mt-1" />
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Feature Flags</CardTitle>
            <CardDescription>Enable/disable platform features</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { label: 'AI Knowledge Base', enabled: true },
              { label: 'Document Auto-Verification', enabled: true },
              { label: 'Email Notifications', enabled: true },
              { label: 'SMS Notifications', enabled: false },
              { label: 'WhatsApp Integration', enabled: false },
              { label: 'Public Registration', enabled: true },
            ].map((f) => (
              <div key={f.label} className="flex items-center justify-between py-2">
                <span className="text-sm text-slate-700 dark:text-slate-300">{f.label}</span>
                <Badge variant={f.enabled ? 'success' : 'secondary'}>{f.enabled ? 'Enabled' : 'Disabled'}</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="flex justify-end">
        <Button><Save className="w-4 h-4 mr-2" /> Save Changes</Button>
      </div>
    </div>
  )
}
