import requests
import json
import difflib
from datetime import datetime
from typing import Dict, Any, List, Tuple
import os


class APIComparator:
    def __init__(self):
        self.results = []
        
    def compare_apis(self, name: str, old_url: str, new_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """API 응답을 비교하고 결과를 반환"""
        try:
            # Old API 호출
            old_response = requests.get(old_url, headers=headers, timeout=30)
            old_data = old_response.json() if old_response.status_code == 200 else None
            
            # New API 호출
            new_response = requests.get(new_url, headers=headers, timeout=30)
            new_data = new_response.json() if new_response.status_code == 200 else None
            
            # 비교 결과
            result = {
                'name': name,
                'old_status': old_response.status_code,
                'new_status': new_response.status_code,
                'old_response_time': old_response.elapsed.total_seconds(),
                'new_response_time': new_response.elapsed.total_seconds(),
                'data_match': self._compare_data(old_data, new_data),
                'old_data': old_data,
                'new_data': new_data,
                'diff': self._generate_diff(old_data, new_data)
            }
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                'name': name,
                'error': str(e),
                'old_status': None,
                'new_status': None
            }
            self.results.append(error_result)
            return error_result
    
    def _compare_data(self, old_data: Any, new_data: Any) -> bool:
        """데이터가 동일한지 비교"""
        if old_data is None and new_data is None:
            return True
        if old_data is None or new_data is None:
            return False
        
        # 데이터를 id 기준으로 정렬 후 비교
        old_sorted = self._sort_data_by_id(old_data)
        new_sorted = self._sort_data_by_id(new_data)
        
        # JSON을 정렬된 문자열로 변환하여 비교
        old_str = json.dumps(old_sorted, sort_keys=True, ensure_ascii=False)
        new_str = json.dumps(new_sorted, sort_keys=True, ensure_ascii=False)
        return old_str == new_str
    
    def _sort_data_by_id(self, data: Any) -> Any:
        """데이터를 id 기준으로 정렬"""
        if isinstance(data, dict):
            sorted_dict = {}
            for key, value in data.items():
                sorted_dict[key] = self._sort_data_by_id(value)
            return sorted_dict
        elif isinstance(data, list):
            if all(isinstance(item, dict) and 'id' in item for item in data):
                return sorted(data, key=lambda x: str(x['id']))
            else:
                return [self._sort_data_by_id(item) for item in data]
        else:
            return data
    
    def _generate_diff(self, old_data: Any, new_data: Any) -> List[str]:
        """차이점을 생성"""
        if old_data is None or new_data is None:
            return []
        
        # 정렬된 데이터로 diff 생성
        old_sorted = self._sort_data_by_id(old_data)
        new_sorted = self._sort_data_by_id(new_data)
        
        old_json = json.dumps(old_sorted, indent=2, sort_keys=True, ensure_ascii=False)
        new_json = json.dumps(new_sorted, indent=2, sort_keys=True, ensure_ascii=False)
        
        diff = list(difflib.unified_diff(
            old_json.splitlines(keepends=True),
            new_json.splitlines(keepends=True),
            fromfile='Old API',
            tofile='New API',
            lineterm=''
        ))
        
        return diff
    
    def generate_html_report(self, output_path: str = None) -> str:
        """HTML 리포트 생성"""
        if output_path is None:
            output_path = f"api_comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = self._create_html_template()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path
    
    def _create_html_template(self) -> str:
        """HTML 템플릿 생성"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.get('data_match', False))
        failed = total - passed
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>API 비교 리포트</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .api-result {{ border: 1px solid #ddd; margin: 10px 0; border-radius: 5px; }}
        .api-header {{ background: #e9e9e9; padding: 10px; font-weight: bold; }}
        .api-content {{ padding: 15px; }}
        .success {{ border-left: 5px solid #4CAF50; }}
        .failure {{ border-left: 5px solid #f44336; }}
        .error {{ border-left: 5px solid #ff9800; }}
        .diff {{ background: #f9f9f9; padding: 10px; border-radius: 3px; overflow-x: auto; }}
        pre {{ white-space: pre-wrap; font-size: 12px; }}
        .stats {{ display: flex; gap: 20px; }}
        .stat-box {{ padding: 10px; border-radius: 5px; text-align: center; min-width: 100px; }}
        .stat-total {{ background: #2196F3; color: white; }}
        .stat-passed {{ background: #4CAF50; color: white; }}
        .stat-failed {{ background: #f44336; color: white; }}
    </style>
</head>
<body>
    <h1>API 비교 리포트</h1>
    <div class="summary">
        <h2>요약</h2>
        <div class="stats">
            <div class="stat-box stat-total">
                <div>총 API</div>
                <div><strong>{total}</strong></div>
            </div>
            <div class="stat-box stat-passed">
                <div>성공</div>
                <div><strong>{passed}</strong></div>
            </div>
            <div class="stat-box stat-failed">
                <div>실패</div>
                <div><strong>{failed}</strong></div>
            </div>
        </div>
        <p>생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>상세 결과</h2>
"""
        
        for result in self.results:
            if 'error' in result:
                html += self._create_error_section(result)
            else:
                html += self._create_result_section(result)
        
        html += """
</body>
</html>
"""
        return html
    
    def _create_result_section(self, result: Dict[str, Any]) -> str:
        """결과 섹션 생성"""
        status_class = 'success' if result['data_match'] else 'failure'
        status_text = '✅ 일치' if result['data_match'] else '❌ 불일치'
        
        # Old Response 전체 내용
        old_response_html = ''
        if result.get('old_data'):
            old_json = json.dumps(result['old_data'], indent=2, ensure_ascii=False)
            old_response_html = f"""
            <h4>Old API Response:</h4>
            <div class="diff">
                <pre>{old_json}</pre>
            </div>
            """
        
        # New Response 전체 내용
        new_response_html = ''
        if result.get('new_data'):
            new_json = json.dumps(result['new_data'], indent=2, ensure_ascii=False)
            new_response_html = f"""
            <h4>New API Response:</h4>
            <div class="diff">
                <pre>{new_json}</pre>
            </div>
            """
        
        # Diff 내용 (불일치할 때만)
        diff_html = ''
        if not result['data_match'] and result['diff']:
            diff_content = ''.join(result['diff'])
            diff_html = f"""
            <h4>차이점 (Diff):</h4>
            <div class="diff">
                <pre>{diff_content}</pre>
            </div>
            """
        
        return f"""
    <div class="api-result {status_class}">
        <div class="api-header">
            {result['name']} - {status_text}
        </div>
        <div class="api-content">
            <p><strong>Old API 상태:</strong> {result['old_status']} ({result['old_response_time']:.3f}s)</p>
            <p><strong>New API 상태:</strong> {result['new_status']} ({result['new_response_time']:.3f}s)</p>
            {diff_html}
            {old_response_html}
            {new_response_html}
        </div>
    </div>
"""
    
    def _create_error_section(self, result: Dict[str, Any]) -> str:
        """에러 섹션 생성"""
        return f"""
    <div class="api-result error">
        <div class="api-header">
            {result['name']} - ⚠️ 에러
        </div>
        <div class="api-content">
            <p><strong>에러:</strong> {result['error']}</p>
        </div>
    </div>
"""