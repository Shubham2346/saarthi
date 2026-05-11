'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/lib/auth'
import styles from './Sidebar.module.css'

const NAV_ITEMS = [
  { href: '/dashboard', label: 'Dashboard', icon: '📊' },
  { href: '/chat', label: 'Ask Saarthi', icon: '💬' },
  { href: '/tasks', label: 'My Tasks', icon: '📋' },
]

const ADMIN_ITEMS = [
  { href: '/admin/knowledge', label: 'Knowledge Base', icon: '📚' },
]

export default function Sidebar() {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  const isAdmin = user?.role === 'admin'

  return (
    <aside className={styles.sidebar}>
      <div className={styles.logo}>
        <span className={styles.logoIcon}>🎓</span>
        <span className={styles.logoText}>Saarthi</span>
      </div>

      <nav className={styles.nav}>
        <div className={styles.section}>
          <span className={styles.sectionLabel}>Main</span>
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`${styles.navItem} ${pathname === item.href ? styles.active : ''}`}
            >
              <span className={styles.navIcon}>{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          ))}
        </div>

        {isAdmin && (
          <div className={styles.section}>
            <span className={styles.sectionLabel}>Admin</span>
            {ADMIN_ITEMS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={`${styles.navItem} ${pathname.startsWith(item.href) ? styles.active : ''}`}
              >
                <span className={styles.navIcon}>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        )}
      </nav>

      <div className={styles.userSection}>
        <div className={styles.userInfo}>
          <div className={styles.avatar}>
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt="" referrerPolicy="no-referrer" />
            ) : (
              <span>{user?.full_name?.[0] || '?'}</span>
            )}
          </div>
          <div className={styles.userMeta}>
            <span className={styles.userName}>{user?.full_name || 'Student'}</span>
            <span className={styles.userRole}>{user?.role || 'student'}</span>
          </div>
        </div>
        <button onClick={logout} className={styles.logoutBtn} title="Sign out">
          ↗
        </button>
      </div>
    </aside>
  )
}
