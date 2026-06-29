import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './forgot-password.html',
  styleUrl: './forgot-password.css',
})
export class ForgotPassword {
  email = '';
  isLoading = false;
  successMsg = '';
  errorMsg = '';

  constructor(private authService: Auth) { }

  onSubmit(): void {
    this.errorMsg = '';
    this.successMsg = '';
    this.isLoading = true;

    this.authService.postData('forgot-password', { email: this.email }).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.successMsg = res.message;
      },
      error: (err) => {
        this.isLoading = false;
        this.errorMsg = err.error?.message || 'Something went wrong!';
      }
    });
  }
}
