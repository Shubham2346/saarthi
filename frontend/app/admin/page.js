'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { api } from '@/lib/api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import AppShell from '@/components/AppShell'
import {
  Users, FileText, CheckSquare, Ticket, TrendingUp, AlertCircle,
  ArrowUp, ArrowDown, RefreshCw, GraduationCap, UserPlus,
  ClipboardCheck, ChevronRight, BarChart3, School, Shield, Activity
} from 'lucide-react'
import { useRouter } from 'next/navigation'

const colors = {
  indigo: 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400',
  emerald: 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  amber: 'bg-amber-100 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400',
  rose: 'bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400',
  blue: 'bg-blue-100 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400',
  slate: 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400',
}

function StatCard({ label, value, icon: Icon, color = 'indigo', trend, delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
      className="stats-card"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <p className="text-2xl font-bold text-foreground mt-0.5">{value}</p>
          {trend && (
            <span className={`text-xs font-medium mt-0.5 inline-flex items-center gap-0.5 ${trend > 0 ? 'text-emerald-600' : 'text-red-500'}`}>
              {trend > 0 ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />} {Math.abs(trend)}%
            </span>
          )}
        </div>
        {Icon && (
          <div className={`h-11 w-11 rounded-xl flex items-center justify-center flex-shrink-0 ${colors[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function AdminDashboard() {
  return <AppShell><AdminDashboard_ /></AppShell>
}
function AdminDashboard_() {
  const { user } = useAuth()
  const router = useRouter()
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const data = await api.get('/admin/dashboard')
        setStats(data)
      } catch (e) {
        console.error('Failed to load admin dashboard', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-48" />
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
        </div>
      </div>
    )
  }

  const pendingDocs = stats?.pending_documents || 0
  const activeTickets = stats?.active_tickets || 0
  const completionRate = stats?.completion_rate || 0

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Shield className="w-5 h-5 text-indigo-500" />
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">Admin Operations</h1>
          </div>
          <p className="text-muted-foreground">Manage admissions, verify documents, oversee students</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => window.location.reload()}>
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
        </Button>
      </motion.div>

      {/* Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Students" value={stats?.total_students || 0} icon={Users} color="indigo" trend={12} delay={0.1} />
        <StatCard label="Pending Documents" value={pendingDocs} icon={FileText} color="amber" trend={-5} delay={0.15} />
        <StatCard label="Active Tickets" value={activeTickets} icon={Ticket} color="rose" trend={3} delay={0.2} />
        <StatCard label="Completion Rate" value={`${completionRate}%`} icon={TrendingUp} color="emerald" trend={8} delay={0.25} />
      </div>

      {/* Pending Actions */}
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Card>
            <CardHeader>
              <CardTitle>Pending Verifications</CardTitle>
              <CardDescription>Documents awaiting your review</CardDescription>
            </CardHeader>
            <CardContent>
              {pendingDocs > 0 ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-500/5 border border-amber-200/50 dark:border-amber-800/50">
                    <AlertCircle className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-amber-800 dark:text-amber-300">{pendingDocs} document(s) pending</p>
                      <p className="text-xs text-amber-600 dark:text-amber-400">Review and verify uploaded student documents</p>
                    </div>
                  </div>
                  <Button onClick={() => router.push('/admin/documents')} className="w-full">
                    Review Documents <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
                  <ClipboardCheck className="w-5 h-5" /> All documents verified
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
          <Card>
            <CardHeader>
              <CardTitle>Support Tickets</CardTitle>
              <CardDescription>Open tickets requiring attention</CardDescription>
            </CardHeader>
            <CardContent>
              {activeTickets > 0 ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-3 p-3 rounded-lg bg-rose-50 dark:bg-rose-500/5 border border-rose-200/50 dark:border-rose-800/50">
                    <Ticket className="w-5 h-5 text-rose-600 dark:text-rose-400" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-rose-800 dark:text-rose-300">{activeTickets} active ticket(s)</p>
                      <p className="text-xs text-rose-600 dark:text-rose-400">Student support requests</p>
                    </div>
                  </div>
                  <Button variant="outline" onClick={() => router.push('/admin/tickets')} className="w-full">
                    View Tickets <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-sm text-emerald-600 dark:text-emerald-400">
                  <CheckSquare className="w-5 h-5" /> No open tickets
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Admission Pipeline */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="section-title">Admission Pipeline</h2>
            <p className="section-desc">Application lifecycle breakdown</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => router.push('/admin/analytics')}>
            <BarChart3 className="w-3.5 h-3.5 mr-1.5" /> Analytics
          </Button>
        </div>
        <Card>
          <CardContent className="p-6">
            <div className="grid gap-4 sm:grid-cols-5">
              {[
                { label: 'Applied', value: stats?.applied || 0, color: 'bg-blue-500', pct: 40 },
                { label: 'Docs Uploaded', value: stats?.documents_uploaded || 0, color: 'bg-amber-500', pct: 30 },
                { label: 'Verified', value: stats?.verified || 0, color: 'bg-indigo-500', pct: 20 },
                { label: 'Approved', value: stats?.approved || 0, color: 'bg-emerald-500', pct: 15 },
                { label: 'Enrolled', value: stats?.enrolled || 0, color: 'bg-purple-500', pct: 10 },
              ].map((stage) => (
                <div key={stage.label} className="text-center p-4 rounded-xl bg-accent/30">
                  <div className={`h-2 w-full rounded-full mb-3 ${stage.color} opacity-60`} style={{ width: `${stage.pct}%` }} />
                  <p className="text-2xl font-bold text-foreground">{stage.value}</p>
                  <p className="text-xs text-muted-foreground mt-0.5">{stage.label}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions + Activity */}
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common admin tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-2">
                {[
                  { label: 'Manage Students', href: '/admin/students', icon: Users },
                  { label: 'Assign Mentors', href: '/admin/mentors', icon: UserPlus },
                  { label: 'View Applications', href: '/admin/applications', icon: GraduationCap },
                  { label: 'Knowledge Base', href: '/admin/knowledge', icon: FileText },
                ].map((link) => {
                  const Icon = link.icon
                  return (
                    <button key={link.label} onClick={() => router.push(link.href)}
                      className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-accent/50 transition-colors text-left">
                      <div className="h-8 w-8 rounded-lg bg-indigo-100 dark:bg-indigo-500/10 flex items-center justify-center">
                        <Icon className="w-4 h-4 text-indigo-600 dark:text-indigo-400" />
                      </div>
                      <span className="text-sm font-medium text-foreground flex-1">{link.label}</span>
                      <ChevronRight className="w-4 h-4 text-muted-foreground" />
                    </button>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
          <Card>
            <CardHeader>
              <CardTitle>Recent Activity</CardTitle>
              <CardDescription>Latest actions in the system</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { action: 'New student registered', time: '5 min ago', icon: UserPlus, color: 'text-indigo-500' },
                  { action: 'Document verified for Rahul S.', time: '15 min ago', icon: ClipboardCheck, color: 'text-emerald-500' },
                  { action: 'Application approved for Priya M.', time: '1 hour ago', icon: CheckSquare, color: 'text-emerald-500' },
                  { action: 'Support ticket #1024 resolved', time: '2 hours ago', icon: Ticket, color: 'text-blue-500' },
                  { action: 'Mentor assigned to 3 students', time: '3 hours ago', icon: UserPlus, color: 'text-indigo-500' },
                ].map((activity, i) => {
                  const Icon = activity.icon
                  return (
                    <div key={i} className="flex items-center gap-3 text-sm">
                      <Icon className={`w-4 h-4 ${activity.color} flex-shrink-0`} />
                      <span className="text-foreground flex-1">{activity.action}</span>
                      <span className="text-muted-foreground text-xs">{activity.time}</span>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}
