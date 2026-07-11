import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { Auth } from '../../../services/auth/auth';
import { Common } from '../../../services/common/common';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  private authService = inject(Auth);
  private commonService = inject(Common);
  private router = inject(Router);

  // Form fields
  formData = {
    email: '',
    password: ''
  };

  // UI state
  isLoading = false;
  errorMsg = '';

  constructor(
  ) {
    // Agar already logged in hai toh home pe bhejo
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/home']);
    }
  }

  onSubmit(): void {
    this.errorMsg = '';
    this.isLoading = true;

    this.commonService.postData('login', this.formData).subscribe({
      next: (response) => {
        console.log('Login successful:', response);
        this.isLoading = false;
        let data = response?.data;
        // Token aur user info save karo
        this.authService.saveToken(data?.token, data?.user);

        // Home page pe redirect
        this.router.navigate(['/dashboard/home']);
      },
      error: (err) => {
        console.error('Login failed:', err);
        this.isLoading = false;
        this.errorMsg = err.error?.message || 'Something went wrong!';
      }
    });
  }
}
