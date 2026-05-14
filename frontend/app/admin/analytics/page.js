'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { BarChart3, TrendingUp, Users, FileText } from 'lucide-react'

export default function AdminAnalytics() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Analytics</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400">Admission pipeline and performance metrics</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Admission Funnel</CardTitle>
            <CardDescription>Student progression through stages</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { stage: 'Applied', pct: 100, count: 245 },
                { stage: 'Documents Uploaded', pct: 78, count: 191 },
                { stage: 'Verified', pct: 62, count: 152 },
                { stage: 'Approved', pct: 45, count: 110 },
                { stage: 'Enrolled', pct: 32, count: 78 },
              ].map((item) => (
                <div key={item.stage}>
                  <div className="flex items-center justify-between text-sm mb-1">
                    <span className="text-slate-700 dark:text-slate-300">{item.stage}</span>
                    <span className="text-slate-500 dark:text-slate-400">{item.count} ({item.pct}%)</span>
                  </div>
                  <div className="h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-600 rounded-full transition-all" style={{ width: `${item.pct}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Department Distribution</CardTitle>
            <CardDescription>Applications by department</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { dept: 'Computer Engineering', count: 89, pct: 36 },
                { dept: 'IT', count: 52, pct: 21 },
                { dept: 'Electronics & Telecomm.', count: 41, pct: 17 },
                { dept: 'Mechanical', count: 33, pct: 13 },
                { dept: 'Civil', count: 18, pct: 7 },
                { dept: 'Other', count: 12, pct: 5 },
              ].map((item) => (
                <div key={item.dept} className="flex items-center gap-3">
                  <div className="flex-1">
                    <div className="flex items-center justify-between text-sm mb-1">
                      <span className="text-slate-700 dark:text-slate-300">{item.dept}</span>
                      <span className="text-slate-500 text-xs">{item.count}</span>
                    </div>
                    <div className="h-1.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${item.pct}%` }} />
                    </div>
                  </div>
                  <span className="text-xs font-medium text-slate-500 w-8 text-right">{item.pct}%</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
