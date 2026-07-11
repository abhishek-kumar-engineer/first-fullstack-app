import { computed, Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class LoaderService {
  private activeRequests = signal(0);

  readonly loading = computed(() => this.activeRequests() > 0);

  show(): void {
    this.activeRequests.update(value => value + 1);
  }

  hide(): void {
    this.activeRequests.update(value => Math.max(0, value - 1));
  }
}
