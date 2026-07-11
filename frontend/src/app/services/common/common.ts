import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class Common {
  private http = inject(HttpClient);

  getData(url: string, queryParams?: any): Observable<any> {
    return this.http.get(`${environment.apiUrl}/${url}`, { params: queryParams });
  }

  // common postData method for all api calls
  postData(url: string, data: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/${url}`, data);
  }

  // common postFormData method — file uploads ke liye (avatar, documents, etc.)
  // Content-Type header manually set NAHI karte — browser khud boundary ke saath
  // multipart/form-data set karta hai FormData body dekh kar
  postFormData(url: string, formData: FormData): Observable<any> {
    return this.http.post(`${environment.apiUrl}/${url}`, formData);
  }

}
