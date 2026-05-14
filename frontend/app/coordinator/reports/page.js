'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { BarChart3, Download } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function CoordinatorReports() {
  const stats = [
    { label: 'Total Applications', value: '156' },
    { label: 'Pending Review', value: '23' },
    { label: 'Approved', value: '89' },
    { label: 'Enrolled', value: '44' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Reports</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Department admission reports and analytics</p>
        </div>
        <Button variant="outline" size="sm"><Download className="w-4 h-4 mr-1" /> Export</Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((s) => (
          <Card key={s.label}>
            <CardContent className="p-6 text-center">
              <p className="text-3xl font-bold text-slate-900 dark:text-white">{s.value}</p>
              <p className="text-sm text-slate-500 mt-1">{s.label}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Admission Trends</CardTitle>
          <CardDescription>Weekly application trends for your department</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-48 text-slate-400">
            <BarChart3 className="w-8 h-8 mr-2" />
            <span>Chart visualization available in full dashboard</span>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
