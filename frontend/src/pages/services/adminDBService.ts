export async function createGlobalSchoolDB(backendUrl: string) {
    try {
      const response = await fetch(`${backendUrl}/database/admin/create-global-school-db`, {
        method: 'POST',
      });
      if (response.status === 200) {
        const result = await response.json();
        console.log(result);
        alert('Global school DB created!');
      } else {
        alert('Global school DB creation failed!');
      }
    } catch (error) {
      console.error('Error creating global school db:', error);
      alert('Global school DB creation failed!');
    }
  }