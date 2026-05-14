'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { FileText, Plus } from 'lucide-react'

export default function MentorNotes() {
  const [notes, setNotes] = useState([
    { id: 1, student: 'Rahul Sharma', content: 'Discussed project options for final year. Suggested Machine Learning domain.', date: '2026-05-10' },
    { id: 2, student: 'Priya Patel', content: 'Academic performance review. CGPA 7.8. Need to focus on DSA for placements.', date: '2026-05-08' },
  ])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Mentoring Notes</h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">Track student interactions and progress</p>
        </div>
        <Button size="sm"><Plus className="w-4 h-4 mr-1" /> Add Note</Button>
      </div>

      <div className="space-y-3">
        {notes.map((note) => (
          <Card key={note.id}>
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <FileText className="w-5 h-5 text-indigo-600 dark:text-indigo-400 mt-0.5" />
                  <div>
                    <p className="font-medium text-slate-900 dark:text-white">{note.student}</p>
                    <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{note.content}</p>
                  </div>
                </div>
                <span className="text-xs text-slate-400">{note.date}</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
