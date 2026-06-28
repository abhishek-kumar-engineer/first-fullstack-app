import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Auth } from '../../services/auth';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  // Form fields
  formData = {
    email: '',
    password: ''
  };

  // UI state
  isLoading = false;
  errorMsg = '';

  constructor(
    private authService: Auth,
    private router: Router
  ) {
    // Agar already logged in hai toh home pe bhejo
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/home']);
    }
  }

  onSubmit(): void {
    this.errorMsg = '';
    this.isLoading = true;

    this.authService.login(this.formData).subscribe({
      next: (response) => {
        // console.log('Login successful:', response);
        this.isLoading = false;

        // Token aur user info save karo
        this.authService.saveToken(response.token, response.user);

        // Home page pe redirect
        this.router.navigate(['/home']);
      },
      error: (err) => {
        console.error('Login failed:', err);
        this.isLoading = false;
        this.errorMsg = err.error?.message || 'Something went wrong!';
      }
    });
  }
}
