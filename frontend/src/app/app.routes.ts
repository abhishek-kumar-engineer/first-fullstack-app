// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { Login } from './pages/user-auth/login/login';
import { Register } from './pages/user-auth/register/register';
import { Home } from './pages/home/home';
import { authGuard } from './guards/auth-guard';
import { ForgotPassword } from './pages/user-auth/forgot-password/forgot-password';
import { ResetPassword } from './pages/user-auth/reset-password/reset-password';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'forgot-password', component: ForgotPassword },
  { path: 'reset-password', component: ResetPassword },
  {
    path: 'home',
    component: Home,
    canActivate: [authGuard]   // ← bina login ke home nahi khulega
  }
];