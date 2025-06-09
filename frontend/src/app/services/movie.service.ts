import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class MovieService {
  private apiUrl = 'http://localhost:8005/api/movies/';

  constructor(private http: HttpClient) {}

  getMovies(cursor?: string): Observable<any> {
    let params = new HttpParams();

    if (cursor !== undefined) {
      params = params.set('cursor', cursor);
    }

    return this.http.get<any>(this.apiUrl, { params });
  }
}
