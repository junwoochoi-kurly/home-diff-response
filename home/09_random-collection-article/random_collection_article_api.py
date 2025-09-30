from home.api_comparator import APIComparator
from home.config.domains import OLD_API_DOMAIN, NEW_API_DOMAIN, COMMON_HEADERS


def main():
    """Beauty main-banner API 테스트"""
    
    # 공통 헤더
    headers = COMMON_HEADERS
    
    # API URLs
    old_url = f'{OLD_API_DOMAIN}/api/public/v3/sites/market/sections/538/random-collection-article'
    new_url = f'{NEW_API_DOMAIN}/public/v3/sites/market/sections/538/random-collection-article'
    
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