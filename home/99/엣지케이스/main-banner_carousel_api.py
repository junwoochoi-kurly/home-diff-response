from home.api_comparator import APIComparator
from home.config.domains import OLD_API_DOMAIN, NEW_API_DOMAIN


def main():
    """Beauty main-banner API 테스트"""
    
    # 공통 헤더
    headers = {
        'User-Agent': 'OS/iOS (14.3) AppVersion/205.36.0 (703) Device/iPhone11,2 Kurly/2.36.0 (703) DeviceID/E979246B-1358-4EF0-9CF6-4680CB986311',
        'X-KURLY-CLUSTER-CENTER-CODE': 'CC02',
        'X-KURLY-DELIVERY-TYPE': 'direct',
        'X-KURLY-MEMBER-UUID': 'f0199879-cba2-57de-92c5-9e7db9366816',
        'X-KURLY-MEMBER-NO': '25332847',
        'X-KURLY-CART-ID': 'd50adc30-0dfe-458e-9d14-8d2a1962ece8',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjYXJ0X2lkIjoiZjM0YTNmYzAtNGViYi00MDU2LWE1ZDEtMmMwYzY3YTczYTFmIiwiaXNfZ3Vlc3QiOmZhbHNlLCJ1dWlkIjoiNWE5NmMyMGYtNzg2My00NTQ3LWFhYmMtNTQ5ZDhlM2E5OGQxIiwibV9ubyI6NTIwNDQ2OTEsIm1faWQiOiJqdW53b28uY2hvaUBrdXJseWNvcnAuY29tIiwibGV2ZWwiOjEwMCwic3ViIjoiNWE5NmMyMGYtNzg2My00NTQ3LWFhYmMtNTQ5ZDhlM2E5OGQxIiwiaXNzIjoiaHR0cHM6Ly9hcGkuZGV2Lmt1cmx5LnNlcnZpY2VzL3YzL2F1dGgvbG9naW4iLCJpYXQiOjE3NTkyMTEwMTYsImV4cCI6MTc1OTIxNDYxNiwibmJmIjoxNzU5MjExMDE2LCJqdGkiOiJRdGhqQ1VRYU5BSEQzblpqIn0.UPVvGJxXtDKL6oYVKFgmsbmgHHp4oCTmQsQs4yDU0u0'
    }
    
    # API URLs
    old_url = f'{OLD_API_DOMAIN}/api/public/v3/sites/market/sections/245/main_banner_carousel'
    new_url = f'{NEW_API_DOMAIN}/public/v3/sites/market/sections/245/main_banner_carousel'
    
    # 비교 실행
    comparator = APIComparator()
    result = comparator.compare_apis(
        name="Beauty Main Banner API",
        old_url=old_url,
        new_url=new_url,
        headers=headers
    )
    
    # 결과 출력
    print(f"API 비교 결과: {result['name']}")
    print(f"Old API 상태: {result.get('old_status', 'Error')}")
    print(f"New API 상태: {result.get('new_status', 'Error')}")
    print(f"데이터 일치: {'✅' if result.get('data_match', False) else '❌'}")
    
    if 'error' in result:
        print(f"에러 발생: {result['error']}")
    
    # HTML 리포트 생성
    report_path = comparator.generate_html_report('report.html')
    print(f"HTML 리포트 생성완료: {report_path}")
    
    return result


if __name__ == "__main__":
    main()