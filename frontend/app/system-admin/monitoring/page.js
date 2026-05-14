'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Activity, Server, Database, Cpu, Wifi } from 'lucide-react'

export default function SysAdminMonitoring() {
  const services = [
    { name: 'API Server', status: 'healthy', uptime: '99.9%', icon: Server },
    { name: 'Database', status: 'healthy', uptime: '99.95%', icon: Database },
    { name: 'Vector Store', status: 'healthy', uptime: '99.8%', icon: Cpu },
    { name: 'Ollama (optional)', status: 'disconnected', uptime: '-', icon: Cpu },
    { name: 'Redis Cache', status: 'healthy', uptime: '99.9%', icon: Wifi },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">System Monitoring</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Platform health and performance metrics</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Service Status</CardTitle>
            <CardDescription>Current health of all services</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {services.map((s) => {
              const Icon = s.icon
              return (
                <div key={s.name} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                  <div className="flex items-center gap-3">
                    <Icon className="w-5 h-5 text-slate-600 dark:text-slate-400" />
                    <div>
                      <p className="text-sm font-medium text-slate-900 dark:text-white">{s.name}</p>
                      <p className="text-xs text-slate-500">Uptime: {s.uptime}</p>
                    </div>
                  </div>
                  <Badge variant={s.status === 'healthy' ? 'success' : 'destructive'}>{s.status}</Badge>
                </div>
              )
            })}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>System administration tasks</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { label: 'Clear Cache', desc: 'Flush Redis cache' },
              { label: 'Re-index Knowledge Base', desc: 'Rebuild ChromaDB vectors' },
              { label: 'Run DB Backup', desc: 'Manual PostgreSQL backup' },
              { label: 'System Health Check', desc: 'Run diagnostics' },
            ].map((action) => (
              <div key={action.label} className="flex items-center justify-between p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">{action.label}</p>
                  <p className="text-xs text-slate-500">{action.desc}</p>
                </div>
                <Activity className="w-4 h-4 text-slate-400" />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
