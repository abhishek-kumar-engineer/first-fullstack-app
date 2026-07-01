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
}
