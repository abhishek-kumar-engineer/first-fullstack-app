// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { Login } from './pages/user-auth/login/login';
import { Register } from './pages/user-auth/register/register';
import { Home } from './pages/home/home';
import { authGuard } from './guards/auth-guard';
import { ForgotPassword } from './pages/user-auth/forgot-password/forgot-password';
import { ResetPassword } from './pages/user-auth/reset-password/reset-password';
import { Dashboard } from './pages/dashboard/dashboard';
import { Profile } from './core/profile/profile';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'forgot-password', component: ForgotPassword },
  { path: 'reset-password', component: ResetPassword },

  // ── Protected — Dashboard wrapper ─────────────
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'home', pathMatch: 'full' },
      {
        path: 'home',
        loadComponent: () => import('./pages/home/home').then(m => m.Home),
        canActivate: [authGuard]
      },
      {
        path: 'profile',
        loadComponent: () => import('./core/profile/profile').then(m => m.Profile),
        canActivate: [authGuard]
      }
    ]
  },

  { path: '**', redirectTo: 'login' }
];