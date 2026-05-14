'use client'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Calendar, Clock, Plus, Users } from 'lucide-react'

export default function MentorSchedule() {
  const meetings = [
    { student: 'Rahul Sharma', date: '2026-05-20', time: '10:00 AM', type: '1-on-1', status: 'scheduled' },
    { student: 'Priya Patel', date: '2026-05-22', time: '2:00 PM', type: '1-on-1', status: 'scheduled' },
    { student: 'Group Session', date: '2026-05-25', time: '11:00 AM', type: 'group', status: 'pending' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Schedule</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Manage mentoring sessions</p>
        </div>
        <Button size="sm"><Plus className="w-4 h-4 mr-1" /> Schedule Meeting</Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upcoming Meetings</CardTitle>
          <CardDescription>Your scheduled mentoring sessions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {meetings.map((m, i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-lg bg-slate-50 dark:bg-slate-800/50">
                <div className="flex items-center gap-3">
                  {m.type === 'group' ? (
                    <Users className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  ) : (
                    <Calendar className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  )}
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">{m.student}</p>
                    <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                      <Calendar className="w-3 h-3" /> {m.date}
                      <Clock className="w-3 h-3 ml-1" /> {m.time}
                    </div>
                  </div>
                </div>
                <Badge variant={m.status === 'scheduled' ? 'info' : 'warning'}>{m.status}</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
