'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/lib/auth'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { motion } from 'framer-motion'
import AppShell from '@/components/AppShell'
import {
  Users, Key, Shield, Activity, Database,
  RefreshCw, Lock, Terminal, Server, HardDrive,
  Cpu, Zap, Globe, CheckCircle, AlertTriangle,
  ChevronRight, Wifi
} from 'lucide-react'
import { useRouter } from 'next/navigation'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const colors = {
  indigo: 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400',
  emerald: 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  amber: 'bg-amber-100 dark:bg-amber-500/10 text-amber-600 dark:text-amber-400',
  rose: 'bg-rose-100 dark:bg-rose-500/10 text-rose-600 dark:text-rose-400',
  blue: 'bg-blue-100 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400',
  purple: 'bg-purple-100 dark:bg-purple-500/10 text-purple-600 dark:text-purple-400',
  slate: 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400',
}

function StatCard({ label, value, icon: Icon, color = 'indigo', delay = 0 }) {
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

const SERVICES = [
  { name: 'API Gateway', icon: Globe, status: 'operational', uptime: '99.9%' },
  { name: 'Database', icon: Database, status: 'operational', uptime: '99.8%' },
  { name: 'Vector Store', icon: HardDrive, status: 'operational', uptime: '99.5%' },
  { name: 'Auth Service', icon: Lock, status: 'operational', uptime: '99.9%' },
  { name: 'Cache (Redis)', icon: Zap, status: 'degraded', uptime: '97.2%' },
  { name: 'AI Pipeline', icon: Cpu, status: 'operational', uptime: '99.7%' },
  { name: 'File Storage', icon: Server, status: 'operational', uptime: '99.9%' },
  { name: 'Monitoring', icon: Activity, status: 'operational', uptime: '99.6%' },
]

export default function SystemAdminDashboard() {
  return <AppShell><SystemAdminDashboard_ /></AppShell>
}
function SystemAdminDashboard_() {
  const { user } = useAuth()
  const router = useRouter()
  const [dashboard, setDashboard] = useState(null)
  const [roles, setRoles] = useState([])
  const [loadingData, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const token = localStorage.getItem('token')
        const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
        const [dashRes, rolesRes] = await Promise.all([
          fetch(`${API_BASE}/sysadmin/dashboard`, { headers }),
          fetch(`${API_BASE}/sysadmin/roles`, { headers }),
        ])
        if (dashRes.ok) setDashboard(await dashRes.json())
        if (rolesRes.ok) setRoles(await rolesRes.json())
      } catch (e) {
        console.error('Failed to load sysadmin data', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loadingData) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-8 w-64" />
        <div className="grid gap-4 md:grid-cols-4">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-28 rounded-xl" />)}
        </div>
      </div>
    )
  }

  const totalUsers = dashboard?.total_users || 0
  const totalRoles = dashboard?.total_roles || roles.length || 5
  const totalPermissions = dashboard?.total_permissions || 0
  const dbStatus = dashboard?.db_status || 'Connected'

  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Terminal className="w-5 h-5 text-rose-500" />
            <h1 className="text-2xl sm:text-3xl font-bold text-foreground">System Administration</h1>
          </div>
          <p className="text-muted-foreground">Enterprise platform control center</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="destructive" className="text-[10px] gap-1.5">
            <Lock className="w-3 h-3" /> Restricted
          </Badge>
          <Button variant="outline" size="sm" onClick={() => window.location.reload()}>
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" /> Refresh
          </Button>
        </div>
      </motion.div>

      {/* System Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Users" value={totalUsers} icon={Users} color="indigo" delay={0.1} />
        <StatCard label="System Roles" value={totalRoles} icon={Key} color="purple" delay={0.15} />
        <StatCard label="Permissions" value={totalPermissions} icon={Shield} color="blue" delay={0.2} />
        <StatCard label="Database" value={dbStatus} icon={Database} color={dbStatus === 'Connected' ? 'emerald' : 'rose'} delay={0.25} />
      </div>

      {/* Service Health */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="section-title">Service Health</h2>
            <p className="section-desc">Real-time system status overview</p>
          </div>
          <Button variant="outline" size="sm" onClick={() => router.push('/system-admin/monitoring')}>
            Details <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </Button>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {SERVICES.map((svc, i) => {
            const SvgIcon = svc.icon
            const isOp = svc.status === 'operational'
            return (
              <motion.div
                key={svc.name}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25 + i * 0.05 }}
                className="bg-card rounded-xl border border-border p-4 hover:shadow-elevated transition-shadow"
              >
                <div className="flex items-center gap-2.5 mb-2">
                  <SvgIcon className="w-4 h-4 text-muted-foreground" />
                  <span className="text-xs font-medium text-foreground">{svc.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`w-1.5 h-1.5 rounded-full ${isOp ? 'bg-emerald-500 shadow-glow-green' : 'bg-amber-500'}`} />
                  <span className={`text-xs font-semibold ${isOp ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'}`}>
                    {isOp ? 'Operational' : 'Degraded'}
                  </span>
                  <span className="text-[10px] text-muted-foreground ml-auto">{svc.uptime}</span>
                </div>
              </motion.div>
            )
          })}
        </div>
      </motion.div>

      {/* Role Distribution + Quick Actions */}
      <div className="grid gap-6 lg:grid-cols-2">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
          <Card>
            <CardHeader>
              <CardTitle>Role Distribution</CardTitle>
              <CardDescription>User count by role across the platform</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {roles.length > 0 ? roles.map((r) => (
                  <div key={r.id} className="flex items-center justify-between p-3 rounded-lg bg-accent/30">
                    <div className="flex items-center gap-2.5">
                      <div className="w-2 h-2 rounded-full bg-indigo-500" />
                      <span className="text-sm font-medium text-foreground capitalize">{r.name.replace(/_/g, ' ')}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-muted-foreground">{r.user_count || 0} users</span>
                      {r.is_system && <Badge variant="secondary" className="text-[10px]">System</Badge>}
                    </div>
                  </div>
                )) : (
                  <p className="text-sm text-muted-foreground">No role data available</p>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}>
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>Common administrative tasks</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-3 sm:grid-cols-2">
                {[
                  { label: 'Manage Users', href: '/system-admin/users', icon: Users, iconClass: 'bg-indigo-100 dark:bg-indigo-500/10 text-indigo-600 dark:text-indigo-400' },
                  { label: 'Roles & Permissions', href: '/system-admin/roles', icon: Key, iconClass: 'bg-purple-100 dark:bg-purple-500/10 text-purple-600 dark:text-purple-400' },
                  { label: 'System Health', href: '/system-admin/monitoring', icon: Activity, iconClass: 'bg-emerald-100 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' },
                  { label: 'Audit Logs', href: '/system-admin/audit', icon: Shield, iconClass: 'bg-blue-100 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400' },
                  { label: 'Platform Settings', href: '/system-admin/settings', icon: Terminal, iconClass: 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400' },
                ].map((action) => {
                  const Icon = action.icon
                  return (
                    <button key={action.label} onClick={() => router.push(action.href)}
                      className="flex items-center gap-3 p-3 rounded-lg border border-border hover:border-indigo-300 dark:hover:border-indigo-700 hover:bg-indigo-50/50 dark:hover:bg-indigo-500/5 transition-all text-left">
                      <div className={`h-9 w-9 rounded-lg flex items-center justify-center flex-shrink-0 ${action.iconClass}`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="text-sm font-medium text-foreground">{action.label}</span>
                    </button>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Security Overview */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
        <Card>
          <CardHeader>
            <CardTitle>Security Status</CardTitle>
            <CardDescription>Platform security overview</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              {[
                { label: 'Authentication', status: 'Active' },
                { label: 'JWT Expiry', status: '60 min' },
                { label: 'Rate Limiting', status: '200/min' },
                { label: 'RBAC', status: 'Enabled' },
                { label: 'Audit Logging', status: 'Active' },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between p-3 rounded-lg bg-accent/30">
                  <span className="text-xs text-muted-foreground">{item.label}</span>
                  <span className="text-xs font-semibold text-emerald-600 dark:text-emerald-400 flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" /> {item.status}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}
