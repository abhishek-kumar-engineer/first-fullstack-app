import { CommonModule } from '@angular/common';
import { Component, inject, signal, OnInit } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Common } from '../../services/common/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { LucideDynamicIcon } from '@lucide/angular';
import { environment } from '../../../environments/environment.development';
import { Router } from '@angular/router';

interface UserProfile {
  id: number;
  name: string;
  email: string;
  avatar_url: string | null;
  bio: string | null;
  phone: string | null;
  user_role: string;
  created_at: string;
  updated_at: string;
}

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatIconModule,
    LucideDynamicIcon
  ],
  templateUrl: './profile.html',
  styleUrl: './profile.css',
})
export class Profile implements OnInit {
  private common = inject(Common);
  private fb = inject(FormBuilder);
  private router = inject(Router);
  
  profile = signal<UserProfile | null>(null);
  isLoading = signal(false);
  isSaving = signal(false);
  selectedFile = signal<File | null>(null);
  previewUrl = signal<string | null>(null);

  profileForm = this.fb.group({
    name: [null, [Validators.required, Validators.minLength(2)]],
    phone: [null],
    bio: ['', [Validators.maxLength(500)]]
  });

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.isLoading.set(true);
    this.common.getData('profile').subscribe({
      next: (res) => {
        this.profile.set(res.data);
        this.profileForm.patchValue({
          name: res.data.name,
          phone: res.data.phone,
          bio: res.data.bio
        });
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  saveProfile(formValue: { name: string | null; bio: string | null; phone: string | null } | any): void {
    if (this.profileForm.invalid) return;
    // console.log('Form Value:', formValue);
    this.isSaving.set(true);
    this.common.putData('profile', formValue?.value).subscribe({
      next: (res) => {
        this.profile.set(res.data);
        this.isSaving.set(false);
      },
      error: () => this.isSaving.set(false)
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    this.selectedFile.set(file);
    this.previewUrl.set(URL.createObjectURL(file));
  }

  cancelAvatarSelection(): void {
    const url = this.previewUrl();
    if (url) URL.revokeObjectURL(url);

    this.selectedFile.set(null);
    this.previewUrl.set(null);
  }

  uploadAvatar(): void {
    const file = this.selectedFile();
    if (!file) return;

    const formData = new FormData();
    formData.append('avatar', file);

    this.common.postFormData('profile/avatar', formData).subscribe({
      next: (res) => {
        this.profile.update(p => p ? { ...p, avatar_url: res.data.avatar_url } : p);
        this.cancelAvatarSelection();
      }
    });
  }

  getAvatarUrl(avatarUrl: string | null): string | null {
    if (!avatarUrl) return null;
    return `${environment.baseUrl}${avatarUrl}`;
  }
}
