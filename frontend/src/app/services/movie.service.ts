import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiUrl = 'http://localhost:8005/api/movies/';

  constructor(private http: HttpClient) {}

  getMoviesWithParams(params: any): Observable<any> {
    return this.http.get<any>(this.apiUrl, { params });
  }

  getFormOptions(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}form-options/`);
  }

  getMovieById(id: string | number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }
}
