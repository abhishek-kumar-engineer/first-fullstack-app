import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Auth } from '../../../services/auth/auth';
import { Common } from '../../../services/common/common';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './forgot-password.html',
  styleUrl: './forgot-password.css',
})
export class ForgotPassword {

  private authService = inject(Auth);
  private commonService = inject(Common);
  
  email = '';
  isLoading = false;
  successMsg = '';
  errorMsg = '';

  constructor() { }

  onSubmit(): void {
    this.errorMsg = '';
    this.successMsg = '';
    this.isLoading = true;

    this.commonService.postData('forgot-password', { email: this.email }).subscribe({
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
