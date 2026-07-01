import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Auth {

  constructor(private http: HttpClient) { }

  // ── Register API call ──────────────────────────────
  register(data: { name: string; email: string; password: string }): Observable<any> {
    return this.http.post(`${environment.apiUrl}/register`, data);
  }

  // ── Login API call ─────────────────────────────────
  login(data: { email: string; password: string }): Observable<any> {
    return this.http.post(`${environment.apiUrl}/login`, data);
  }

  // ── Token save karo localStorage mein ─────────────
  saveToken(token: string, user: any): void {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  }

  // ── Token lo ──────────────────────────────────────
  getToken(): string | null {
    return localStorage?.getItem('token');
  }

  // ── Logged in hai ya nahi check karo ──────────────
  isLoggedIn(): boolean {
    return !!this.getToken();   // token hai → true, nahi → false
  }

  // ── Logout ────────────────────────────────────────
  logout(): Observable<any> {
    return this.http.post(`${environment.apiUrl}/logout`, {});
  }

  // Ye bhi add karo — local cleanup
  clearSession(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // ── User info lo ──────────────────────────────────
  getUser(): any {
    const user = localStorage?.getItem('user');
    return user ? JSON?.parse(user) : null;
  }

  // common postData method for all api calls
  postData(url: string, data: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/${url}`, data);
  }
}
